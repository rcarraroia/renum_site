"""
SICC Audio Processing Tasks - Celery Workers
Processa áudio de forma assíncrona usando TranscriptionService
"""

import os
import tempfile
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import asyncio

from celery import Task
from src.workers.celery_app import celery_app
from src.services.sicc.transcription_service import TranscriptionService
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AudioProcessingTask(Task):
    """Task base para processamento de áudio com retry automático"""
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True

@celery_app.task(base=AudioProcessingTask, bind=True)
def process_audio_file(
    self, 
    file_path: str, 
    agent_id: str,
    language: Optional[str] = None,
    source_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Processa arquivo de áudio completo (transcrição + criação de memórias)
    
    Args:
        file_path: Caminho para o arquivo de áudio
        agent_id: ID do agente
        language: Idioma forçado (opcional)
        source_metadata: Metadados da fonte
        
    Returns:
        Resultado do processamento com transcrição e chunks criados
    """
    try:
        logger.info(f"Iniciando processamento de áudio: {file_path}")
        
        # Validar se arquivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        # Criar serviço de transcrição
        transcription_service = TranscriptionService()
        
        # Executar pipeline completo de forma assíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                transcription_service.transcribe_and_memorize(
                    file_path=file_path,
                    agent_id=agent_id,
                    language=language,
                    source_metadata=source_metadata
                )
            )
        finally:
            loop.close()
        
        logger.info(f"Processamento concluído: {len(result['memory_chunks'])} chunks criados")
        
        # Adicionar informações da task
        result['task_info'] = {
            'task_id': self.request.id,
            'retries': self.request.retries,
            'processed_at': str(asyncio.get_event_loop().time())
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Erro no processamento de áudio: {str(e)}")
        raise

@celery_app.task(base=AudioProcessingTask, bind=True)
def transcribe_audio_only(
    self,
    file_path: str,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Apenas transcreve áudio sem criar memórias
    
    Args:
        file_path: Caminho para o arquivo de áudio
        language: Idioma forçado (opcional)
        
    Returns:
        Resultado da transcrição
    """
    try:
        logger.info(f"Iniciando transcrição: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        transcription_service = TranscriptionService()
        
        # Apenas transcrever
        transcription = transcription_service.transcribe_audio(file_path, language)
        
        result = {
            'transcription': transcription.dict(),
            'task_info': {
                'task_id': self.request.id,
                'retries': self.request.retries,
                'type': 'transcription_only'
            }
        }
        
        logger.info(f"Transcrição concluída: {transcription.duration:.2f}s")
        return result
        
    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}")
        raise

@celery_app.task(base=AudioProcessingTask, bind=True)
def detect_audio_language(self, file_path: str) -> Dict[str, Any]:
    """
    Detecta idioma do áudio
    
    Args:
        file_path: Caminho para o arquivo de áudio
        
    Returns:
        Idioma detectado e confiança
    """
    try:
        logger.info(f"Detectando idioma: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        transcription_service = TranscriptionService()
        language = transcription_service.detect_language(file_path)
        
        result = {
            'language': language,
            'file_path': file_path,
            'task_info': {
                'task_id': self.request.id,
                'type': 'language_detection'
            }
        }
        
        logger.info(f"Idioma detectado: {language}")
        return result
        
    except Exception as e:
        logger.error(f"Erro na detecção de idioma: {str(e)}")
        raise

@celery_app.task(base=AudioProcessingTask, bind=True)
def segment_audio_by_silence(self, file_path: str) -> Dict[str, Any]:
    """
    Segmenta áudio por períodos de silêncio
    
    Args:
        file_path: Caminho para o arquivo de áudio
        
    Returns:
        Lista de segmentos com transcrições
    """
    try:
        logger.info(f"Segmentando áudio: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        transcription_service = TranscriptionService()
        segments = transcription_service.segment_by_silence(file_path)
        
        result = {
            'segments': segments,
            'segments_count': len(segments),
            'file_path': file_path,
            'task_info': {
                'task_id': self.request.id,
                'type': 'audio_segmentation'
            }
        }
        
        logger.info(f"Segmentação concluída: {len(segments)} segmentos")
        return result
        
    except Exception as e:
        logger.error(f"Erro na segmentação: {str(e)}")
        raise

@celery_app.task(base=AudioProcessingTask, bind=True)
def cleanup_temp_audio_file(self, file_path: str) -> Dict[str, Any]:
    """
    Remove arquivo temporário de áudio após processamento
    
    Args:
        file_path: Caminho para o arquivo temporário
        
    Returns:
        Status da limpeza
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.info(f"Arquivo temporário removido: {file_path}")
            return {
                'status': 'removed',
                'file_path': file_path,
                'task_id': self.request.id
            }
        else:
            logger.warning(f"Arquivo não encontrado para remoção: {file_path}")
            return {
                'status': 'not_found',
                'file_path': file_path,
                'task_id': self.request.id
            }
            
    except Exception as e:
        logger.error(f"Erro na limpeza: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'file_path': file_path,
            'task_id': self.request.id
        }

# Função utilitária para criar pipeline de processamento
def create_audio_processing_pipeline(
    file_path: str,
    agent_id: str,
    language: Optional[str] = None,
    source_metadata: Optional[Dict[str, Any]] = None,
    cleanup_after: bool = True
) -> str:
    """
    Cria pipeline completo de processamento de áudio
    
    Args:
        file_path: Caminho para o arquivo de áudio
        agent_id: ID do agente
        language: Idioma forçado (opcional)
        source_metadata: Metadados da fonte
        cleanup_after: Se deve remover arquivo após processamento
        
    Returns:
        Task ID do processamento principal
    """
    # Enfileirar processamento principal
    main_task = process_audio_file.delay(
        file_path=file_path,
        agent_id=agent_id,
        language=language,
        source_metadata=source_metadata
    )
    
    # Enfileirar limpeza após processamento (se solicitado)
    if cleanup_after:
        cleanup_temp_audio_file.apply_async(
            args=[file_path],
            countdown=300  # 5 minutos após o processamento
        )
    
    logger.info(f"Pipeline criado - Task ID: {main_task.id}")
    return main_task.id