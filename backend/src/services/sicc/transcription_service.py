"""
SICC Transcription Service - Whisper Integration
Handles audio transcription using OpenAI Whisper local model
"""

import os
import tempfile
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

import whisper
import librosa
import soundfile as sf
import numpy as np
from pydantic import BaseModel

try:
    from src.services.sicc.embedding_service import EmbeddingService
    from src.services.sicc.memory_service import MemoryService
    from src.utils.logger import get_logger
except ImportError:
    # Fallback para testes
    import logging
    def get_logger(name):
        return logging.getLogger(name)
    
    # Mock services para teste isolado
    class EmbeddingService:
        pass
    
    class MemoryService:
        async def create_chunk(self, **kwargs):
            return {"id": "mock_chunk_id"}

logger = get_logger(__name__)

class TranscriptionSegment(BaseModel):
    """Representa um segmento de transcrição"""
    start_time: float
    end_time: float
    text: str
    confidence: float
    language: str

class TranscriptionResult(BaseModel):
    """Resultado completo da transcrição"""
    segments: List[TranscriptionSegment]
    full_text: str
    language: str
    duration: float
    confidence_avg: float

class TranscriptionService:
    """
    Serviço de transcrição de áudio usando Whisper
    
    Features:
    - Transcrição local com Whisper
    - Detecção automática de idioma
    - Segmentação por silêncio
    - Criação automática de memory chunks
    - Suporte a múltiplos formatos de áudio
    """
    
    def __init__(self):
        self.model = None
        self.model_name = "base"  # base, small, medium, large
        self.embedding_service = EmbeddingService()
        self.memory_service = MemoryService()
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Configurações
        self.supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.min_segment_duration = 2.0  # segundos
        self.silence_threshold = 0.01
        
    def _load_model(self) -> whisper.Whisper:
        """Carrega o modelo Whisper (lazy loading)"""
        if self.model is None:
            logger.info(f"Carregando modelo Whisper: {self.model_name}")
            try:
                self.model = whisper.load_model(self.model_name)
                logger.info("Modelo Whisper carregado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo Whisper: {str(e)}")
                # Fallback para modelo menor
                logger.info("Tentando carregar modelo 'tiny' como fallback")
                self.model = whisper.load_model("tiny")
                self.model_name = "tiny"
                
        return self.model
    
    def _validate_audio_file(self, file_path: str) -> bool:
        """Valida se o arquivo de áudio é suportado"""
        path = Path(file_path)
        
        # Verificar extensão
        if path.suffix.lower() not in self.supported_formats:
            logger.error(f"Formato não suportado: {path.suffix}")
            return False
            
        # Verificar tamanho
        if path.stat().st_size > self.max_file_size:
            logger.error(f"Arquivo muito grande: {path.stat().st_size} bytes")
            return False
            
        # Verificar se arquivo existe
        if not path.exists():
            logger.error(f"Arquivo não encontrado: {file_path}")
            return False
            
        return True
    
    def _preprocess_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Pré-processa o áudio para transcrição
        
        Returns:
            Tuple[audio_data, sample_rate]
        """
        try:
            # Carregar áudio com librosa (normaliza automaticamente)
            audio, sr = librosa.load(file_path, sr=16000)  # Whisper usa 16kHz
            
            # Normalizar volume
            audio = librosa.util.normalize(audio)
            
            logger.info(f"Áudio carregado: {len(audio)/sr:.2f}s, {sr}Hz")
            return audio, sr
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {str(e)}")
            raise
    
    def _segment_by_silence(self, audio: np.ndarray, sr: int) -> List[Tuple[float, float]]:
        """
        Segmenta áudio baseado em períodos de silêncio
        
        Returns:
            Lista de tuplas (start_time, end_time) em segundos
        """
        try:
            # Detectar períodos de não-silêncio
            intervals = librosa.effects.split(
                audio, 
                top_db=20,  # Threshold de silêncio em dB
                frame_length=2048,
                hop_length=512
            )
            
            segments = []
            for start_frame, end_frame in intervals:
                start_time = start_frame / sr
                end_time = end_frame / sr
                duration = end_time - start_time
                
                # Filtrar segmentos muito curtos
                if duration >= self.min_segment_duration:
                    segments.append((start_time, end_time))
            
            logger.info(f"Detectados {len(segments)} segmentos de áudio")
            return segments
            
        except Exception as e:
            logger.error(f"Erro na segmentação: {str(e)}")
            # Fallback: segmento único
            return [(0.0, len(audio) / sr)]
    
    def detect_language(self, file_path: str) -> str:
        """
        Detecta o idioma do áudio
        
        Args:
            file_path: Caminho para o arquivo de áudio
            
        Returns:
            Código do idioma (ex: 'pt', 'en', 'es')
        """
        try:
            if not self._validate_audio_file(file_path):
                raise ValueError("Arquivo de áudio inválido")
                
            model = self._load_model()
            
            # Carregar apenas os primeiros 30 segundos para detecção
            audio, _ = librosa.load(file_path, sr=16000, duration=30)
            
            # Converter para float32 para compatibilidade com Whisper
            audio = audio.astype(np.float32)
            
            # Detectar idioma
            _, probs = model.detect_language(audio)
            detected_language = max(probs, key=probs.get)
            confidence = probs[detected_language]
            
            logger.info(f"Idioma detectado: {detected_language} (confiança: {confidence:.2f})")
            return detected_language
            
        except Exception as e:
            logger.error(f"Erro na detecção de idioma: {str(e)}")
            return "pt"  # Fallback para português
    
    def transcribe_audio(self, file_path: str, language: Optional[str] = None) -> TranscriptionResult:
        """
        Transcreve arquivo de áudio completo
        
        Args:
            file_path: Caminho para o arquivo de áudio
            language: Idioma forçado (opcional, detecta automaticamente se None)
            
        Returns:
            TranscriptionResult com segmentos e texto completo
        """
        try:
            if not self._validate_audio_file(file_path):
                raise ValueError("Arquivo de áudio inválido")
                
            model = self._load_model()
            
            # Detectar idioma se não especificado
            if language is None:
                language = self.detect_language(file_path)
            
            logger.info(f"Iniciando transcrição: {file_path} (idioma: {language})")
            
            # Transcrever com Whisper
            result = model.transcribe(
                file_path,
                language=language,
                word_timestamps=True,
                verbose=False
            )
            
            # Processar segmentos
            segments = []
            for segment in result["segments"]:
                segments.append(TranscriptionSegment(
                    start_time=segment["start"],
                    end_time=segment["end"],
                    text=segment["text"].strip(),
                    confidence=segment.get("avg_logprob", 0.0),
                    language=language
                ))
            
            # Calcular métricas
            full_text = result["text"].strip()
            duration = segments[-1].end_time if segments else 0.0
            confidence_avg = np.mean([s.confidence for s in segments]) if segments else 0.0
            
            transcription_result = TranscriptionResult(
                segments=segments,
                full_text=full_text,
                language=language,
                duration=duration,
                confidence_avg=confidence_avg
            )
            
            logger.info(f"Transcrição concluída: {len(segments)} segmentos, {duration:.2f}s")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {str(e)}")
            raise
    
    def segment_by_silence(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Segmenta áudio por períodos de silêncio e transcreve cada segmento
        
        Args:
            file_path: Caminho para o arquivo de áudio
            
        Returns:
            Lista de segmentos com transcrição individual
        """
        try:
            if not self._validate_audio_file(file_path):
                raise ValueError("Arquivo de áudio inválido")
                
            # Pré-processar áudio
            audio, sr = self._preprocess_audio(file_path)
            
            # Segmentar por silêncio
            silence_segments = self._segment_by_silence(audio, sr)
            
            # Transcrever cada segmento
            model = self._load_model()
            language = self.detect_language(file_path)
            
            transcribed_segments = []
            
            for i, (start_time, end_time) in enumerate(silence_segments):
                try:
                    # Extrair segmento de áudio
                    start_frame = int(start_time * sr)
                    end_frame = int(end_time * sr)
                    segment_audio = audio[start_frame:end_frame]
                    
                    # Salvar segmento temporário
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        sf.write(temp_file.name, segment_audio, sr)
                        temp_path = temp_file.name
                    
                    try:
                        # Transcrever segmento
                        result = model.transcribe(temp_path, language=language)
                        
                        segment_data = {
                            "segment_id": i + 1,
                            "start_time": start_time,
                            "end_time": end_time,
                            "duration": end_time - start_time,
                            "text": result["text"].strip(),
                            "language": language,
                            "confidence": result.get("avg_logprob", 0.0)
                        }
                        
                        transcribed_segments.append(segment_data)
                        logger.info(f"Segmento {i+1} transcrito: {segment_data['text'][:50]}...")
                        
                    finally:
                        # Limpar arquivo temporário
                        os.unlink(temp_path)
                        
                except Exception as e:
                    logger.error(f"Erro no segmento {i+1}: {str(e)}")
                    continue
            
            logger.info(f"Segmentação concluída: {len(transcribed_segments)} segmentos válidos")
            return transcribed_segments
            
        except Exception as e:
            logger.error(f"Erro na segmentação por silêncio: {str(e)}")
            raise
    
    async def create_memory_chunks_from_transcription(
        self, 
        transcription: TranscriptionResult,
        agent_id: str,
        source_metadata: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Cria memory chunks a partir de uma transcrição
        
        Args:
            transcription: Resultado da transcrição
            agent_id: ID do agente
            source_metadata: Metadados adicionais da fonte
            
        Returns:
            Lista de IDs dos memory chunks criados
        """
        try:
            created_chunks = []
            
            # Metadados base
            base_metadata = {
                "source_type": "audio_transcription",
                "language": transcription.language,
                "duration": transcription.duration,
                "confidence_avg": transcription.confidence_avg,
                "segments_count": len(transcription.segments),
                **(source_metadata or {})
            }
            
            # Criar chunk do texto completo
            if transcription.full_text:
                full_text_chunk = await self.memory_service.create_chunk(
                    agent_id=agent_id,
                    content=transcription.full_text,
                    chunk_type="transcription_full",
                    metadata={
                        **base_metadata,
                        "segment_type": "full_text"
                    }
                )
                created_chunks.append(full_text_chunk["id"])
                logger.info(f"Chunk texto completo criado: {full_text_chunk['id']}")
            
            # Criar chunks para segmentos individuais (se houver múltiplos)
            if len(transcription.segments) > 1:
                for i, segment in enumerate(transcription.segments):
                    if len(segment.text.strip()) > 10:  # Filtrar segmentos muito curtos
                        segment_chunk = await self.memory_service.create_chunk(
                            agent_id=agent_id,
                            content=segment.text,
                            chunk_type="transcription_segment",
                            metadata={
                                **base_metadata,
                                "segment_type": "individual",
                                "segment_index": i,
                                "start_time": segment.start_time,
                                "end_time": segment.end_time,
                                "segment_confidence": segment.confidence
                            }
                        )
                        created_chunks.append(segment_chunk["id"])
                        logger.info(f"Chunk segmento {i+1} criado: {segment_chunk['id']}")
            
            logger.info(f"Criados {len(created_chunks)} memory chunks da transcrição")
            return created_chunks
            
        except Exception as e:
            logger.error(f"Erro ao criar memory chunks: {str(e)}")
            raise
    
    async def transcribe_and_memorize(
        self, 
        file_path: str, 
        agent_id: str,
        language: Optional[str] = None,
        source_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Pipeline completo: transcreve áudio e cria memory chunks
        
        Args:
            file_path: Caminho para o arquivo de áudio
            agent_id: ID do agente
            language: Idioma forçado (opcional)
            source_metadata: Metadados da fonte
            
        Returns:
            Resultado completo com transcrição e chunks criados
        """
        try:
            logger.info(f"Iniciando pipeline completo para: {file_path}")
            
            # Executar transcrição em thread separada (CPU-intensive)
            loop = asyncio.get_event_loop()
            transcription = await loop.run_in_executor(
                self.executor,
                self.transcribe_audio,
                file_path,
                language
            )
            
            # Criar memory chunks
            chunk_ids = await self.create_memory_chunks_from_transcription(
                transcription, agent_id, source_metadata
            )
            
            result = {
                "transcription": transcription.dict(),
                "memory_chunks": chunk_ids,
                "stats": {
                    "duration": transcription.duration,
                    "segments_count": len(transcription.segments),
                    "chunks_created": len(chunk_ids),
                    "language": transcription.language,
                    "confidence_avg": transcription.confidence_avg
                }
            }
            
            logger.info(f"Pipeline concluído: {len(chunk_ids)} chunks criados")
            return result
            
        except Exception as e:
            logger.error(f"Erro no pipeline completo: {str(e)}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Retorna lista de formatos de áudio suportados"""
        return list(self.supported_formats)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo Whisper carregado"""
        return {
            "model_name": self.model_name,
            "is_loaded": self.model is not None,
            "supported_formats": self.get_supported_formats(),
            "max_file_size_mb": self.max_file_size / (1024 * 1024),
            "min_segment_duration": self.min_segment_duration
        }