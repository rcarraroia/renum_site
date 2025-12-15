"""
SICC Audio API Routes
Endpoints para upload e processamento de áudio
"""

import os
import tempfile
import uuid
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.api.dependencies import get_current_user
from src.workers.audio_tasks import (
    process_audio_file,
    transcribe_audio_only,
    detect_audio_language,
    segment_audio_by_silence,
    create_audio_processing_pipeline
)
from src.services.sicc.transcription_service import TranscriptionService
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/sicc/audio", tags=["SICC Audio"])

# Modelos Pydantic
class AudioProcessingRequest(BaseModel):
    agent_id: str
    language: Optional[str] = None
    create_memories: bool = True
    source_metadata: Optional[Dict[str, Any]] = None

class AudioProcessingResponse(BaseModel):
    task_id: str
    status: str
    message: str
    file_info: Dict[str, Any]

class TranscriptionResponse(BaseModel):
    transcription: Dict[str, Any]
    task_id: Optional[str] = None

# Configurações
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm'}
UPLOAD_DIR = Path("uploads/audio")

# Criar diretório de upload se não existir
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def validate_audio_file(file: UploadFile) -> None:
    """Valida arquivo de áudio enviado"""
    # Verificar extensão
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado. Formatos aceitos: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Verificar tamanho (aproximado)
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
        )

def save_uploaded_file(file: UploadFile) -> str:
    """Salva arquivo enviado e retorna o caminho"""
    # Gerar nome único
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix.lower()
    temp_filename = f"{file_id}{file_ext}"
    temp_path = UPLOAD_DIR / temp_filename
    
    # Salvar arquivo
    with open(temp_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    logger.info(f"Arquivo salvo: {temp_path} ({len(content)} bytes)")
    return str(temp_path)

@router.post("/upload", response_model=AudioProcessingResponse)
async def upload_audio(
    file: UploadFile = File(...),
    agent_id: str = Form(...),
    language: Optional[str] = Form(None),
    create_memories: bool = Form(True),
    current_user = Depends(get_current_user)
):
    """
    Upload de arquivo de áudio para processamento
    
    - **file**: Arquivo de áudio (wav, mp3, m4a, flac, ogg, webm)
    - **agent_id**: ID do agente que receberá as memórias
    - **language**: Idioma forçado (opcional, detecta automaticamente)
    - **create_memories**: Se deve criar memory chunks (padrão: true)
    """
    try:
        # Validar arquivo
        validate_audio_file(file)
        
        # Salvar arquivo
        file_path = save_uploaded_file(file)
        
        # Metadados da fonte
        source_metadata = {
            "uploaded_by": current_user.get("id"),
            "original_filename": file.filename,
            "content_type": file.content_type,
            "upload_timestamp": str(uuid.uuid1().time)
        }
        
        # Criar pipeline de processamento
        if create_memories:
            task_id = create_audio_processing_pipeline(
                file_path=file_path,
                agent_id=agent_id,
                language=language,
                source_metadata=source_metadata,
                cleanup_after=True
            )
            message = "Arquivo enviado para processamento completo (transcrição + memórias)"
        else:
            # Apenas transcrever
            task = transcribe_audio_only.delay(file_path, language)
            task_id = task.id
            message = "Arquivo enviado para transcrição apenas"
        
        return AudioProcessingResponse(
            task_id=task_id,
            status="queued",
            message=message,
            file_info={
                "filename": file.filename,
                "size": len(open(file_path, 'rb').read()),
                "format": Path(file.filename).suffix.lower(),
                "agent_id": agent_id,
                "language": language
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/task/{task_id}")
async def get_task_status(
    task_id: str,
    current_user = Depends(get_current_user)
):
    """
    Consulta status de uma task de processamento de áudio
    
    - **task_id**: ID da task retornado pelo upload
    """
    try:
        from celery.result import AsyncResult
        
        result = AsyncResult(task_id)
        
        if result.state == 'PENDING':
            response = {
                'task_id': task_id,
                'state': result.state,
                'status': 'Aguardando processamento...'
            }
        elif result.state == 'PROGRESS':
            response = {
                'task_id': task_id,
                'state': result.state,
                'status': 'Processando...',
                'progress': result.info.get('progress', 0)
            }
        elif result.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'state': result.state,
                'status': 'Concluído',
                'result': result.result
            }
        else:  # FAILURE
            response = {
                'task_id': task_id,
                'state': result.state,
                'status': 'Erro no processamento',
                'error': str(result.info)
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Erro ao consultar task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/transcribe-sync", response_model=TranscriptionResponse)
async def transcribe_sync(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    current_user = Depends(get_current_user)
):
    """
    Transcrição síncrona (para arquivos pequenos)
    
    - **file**: Arquivo de áudio pequeno (< 10MB recomendado)
    - **language**: Idioma forçado (opcional)
    """
    try:
        # Validar arquivo
        validate_audio_file(file)
        
        # Verificar tamanho para processamento síncrono
        content = file.file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="Arquivo muito grande para processamento síncrono. Use /upload para arquivos grandes."
            )
        
        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(suffix=Path(file.filename).suffix, delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Transcrever
            transcription_service = TranscriptionService()
            transcription = transcription_service.transcribe_audio(temp_path, language)
            
            return TranscriptionResponse(
                transcription=transcription.dict()
            )
            
        finally:
            # Limpar arquivo temporário
            os.unlink(temp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na transcrição síncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/detect-language")
async def detect_language_endpoint(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """
    Detecta idioma do áudio
    
    - **file**: Arquivo de áudio
    """
    try:
        validate_audio_file(file)
        
        # Salvar temporariamente
        content = file.file.read()
        with tempfile.NamedTemporaryFile(suffix=Path(file.filename).suffix, delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Detectar idioma
            transcription_service = TranscriptionService()
            language = transcription_service.detect_language(temp_path)
            
            return {
                "language": language,
                "filename": file.filename,
                "confidence": "auto-detected"
            }
            
        finally:
            os.unlink(temp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na detecção de idioma: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Lista formatos de áudio suportados
    """
    transcription_service = TranscriptionService()
    model_info = transcription_service.get_model_info()
    
    return {
        "supported_formats": model_info["supported_formats"],
        "max_file_size_mb": model_info["max_file_size_mb"],
        "whisper_model": model_info["model_name"],
        "processing_modes": [
            "async_with_memories",
            "async_transcription_only", 
            "sync_transcription"
        ]
    }

@router.delete("/cleanup/{task_id}")
async def cleanup_task_files(
    task_id: str,
    current_user = Depends(get_current_user)
):
    """
    Força limpeza de arquivos de uma task específica
    
    - **task_id**: ID da task
    """
    try:
        # Aqui você poderia implementar lógica para encontrar e limpar
        # arquivos associados a uma task específica
        
        return {
            "task_id": task_id,
            "status": "cleanup_requested",
            "message": "Limpeza de arquivos solicitada"
        }
        
    except Exception as e:
        logger.error(f"Erro na limpeza: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/stats")
async def get_audio_processing_stats(
    current_user = Depends(get_current_user)
):
    """
    Estatísticas de processamento de áudio
    """
    try:
        # Aqui você poderia implementar estatísticas reais
        # Por enquanto, retorna dados mock
        
        return {
            "total_files_processed": 0,
            "total_duration_minutes": 0,
            "average_processing_time_seconds": 0,
            "supported_formats": len(ALLOWED_EXTENSIONS),
            "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
            "active_tasks": 0,
            "failed_tasks": 0
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")