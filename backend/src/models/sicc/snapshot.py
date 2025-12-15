"""
Snapshot Models - Agent Knowledge Snapshots
Sprint 10 - SICC Implementation

Models for versioned snapshots of agent knowledge state.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class SnapshotType(str, Enum):
    """Snapshot type enumeration"""
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    MILESTONE = "milestone"
    PRE_ROLLBACK = "pre_rollback"


class KnowledgeSnapshotBase(BaseModel):
    """Base knowledge snapshot model"""
    
    snapshot_name: str = Field(..., min_length=1, max_length=200, description="Name of the snapshot")
    description: Optional[str] = Field(None, max_length=1000, description="Description of this snapshot")
    memory_count: int = Field(default=0, ge=0, description="Number of memory chunks in snapshot")
    pattern_count: int = Field(default=0, ge=0, description="Number of behavior patterns in snapshot")
    total_size_bytes: int = Field(default=0, ge=0, description="Total size in bytes")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    @field_validator('snapshot_name')
    @classmethod
    def validate_snapshot_name(cls, v: str) -> str:
        """Validate snapshot name is not empty"""
        if not v or not v.strip():
            raise ValueError("Snapshot name cannot be empty")
        return v.strip()


class KnowledgeSnapshotCreate(KnowledgeSnapshotBase):
    """Model for creating a new knowledge snapshot"""
    
    agent_id: UUID = Field(..., description="Agent ID for this snapshot")
    trigger_reason: str = Field(..., min_length=1, max_length=500, description="Reason for creating snapshot")
    
    @field_validator('trigger_reason')
    @classmethod
    def validate_trigger_reason(cls, v: str) -> str:
        """Validate trigger reason is not empty"""
        if not v or not v.strip():
            raise ValueError("Trigger reason cannot be empty")
        return v.strip()


class KnowledgeSnapshotResponse(KnowledgeSnapshotBase):
    """Model for knowledge snapshot responses"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID for this snapshot")
    version: int = Field(..., description="Snapshot version number")
    trigger_reason: str = Field(..., description="Reason for creating snapshot")
    created_by: Optional[UUID] = Field(None, description="User/ISA that created this snapshot")
    is_active: bool = Field(default=False, description="Whether this is the active snapshot")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True


class SnapshotComparison(BaseModel):
    """Model for comparing two snapshots"""
    
    snapshot_a_id: UUID = Field(..., description="First snapshot ID")
    snapshot_b_id: UUID = Field(..., description="Second snapshot ID")
    memory_added: int = Field(default=0, description="Memory chunks added")
    memory_removed: int = Field(default=0, description="Memory chunks removed")
    memory_modified: int = Field(default=0, description="Memory chunks modified")
    pattern_added: int = Field(default=0, description="Patterns added")
    pattern_removed: int = Field(default=0, description="Patterns removed")
    pattern_modified: int = Field(default=0, description="Patterns modified")
    total_changes: int = Field(default=0, description="Total number of changes")
    change_summary: Dict[str, Any] = Field(default_factory=dict, description="Detailed change summary")
    
    class Config:
        from_attributes = True


class SnapshotRestore(BaseModel):
    """Model for restoring a snapshot"""
    
    snapshot_id: UUID = Field(..., description="Snapshot ID to restore")
    restore_memories: bool = Field(default=True, description="Whether to restore memory chunks")
    restore_patterns: bool = Field(default=True, description="Whether to restore behavior patterns")
    create_backup: bool = Field(default=True, description="Whether to create backup before restore")
    restored_by: UUID = Field(..., description="User/ISA performing the restore")
    reason: str = Field(..., min_length=1, max_length=500, description="Reason for restore")
    
    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate reason is not empty"""
        if not v or not v.strip():
            raise ValueError("Reason cannot be empty")
        return v.strip()


class SnapshotStats(BaseModel):
    """Model for snapshot statistics"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    total_snapshots: int = Field(default=0, description="Total number of snapshots")
    active_snapshot_id: Optional[UUID] = Field(None, description="Currently active snapshot ID")
    oldest_snapshot_date: Optional[datetime] = Field(None, description="Oldest snapshot date")
    newest_snapshot_date: Optional[datetime] = Field(None, description="Newest snapshot date")
    total_size_bytes: int = Field(default=0, description="Total size of all snapshots")
    avg_memory_per_snapshot: float = Field(default=0.0, description="Average memories per snapshot")
    avg_pattern_per_snapshot: float = Field(default=0.0, description="Average patterns per snapshot")
    
    class Config:
        from_attributes = True



class SnapshotCreate(BaseModel):
    """Model for creating a snapshot (simplified for SICC)"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    client_id: UUID = Field(..., description="Client ID")
    snapshot_type: SnapshotType = Field(default=SnapshotType.AUTOMATIC, description="Type of snapshot")


class SnapshotResponse(BaseModel):
    """Model for snapshot responses (matches database schema)"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID")
    client_id: UUID = Field(..., description="Client ID")
    snapshot_type: str = Field(..., description="Type of snapshot")
    memory_count: int = Field(..., description="Number of memories in snapshot")
    pattern_count: int = Field(..., description="Number of patterns in snapshot")
    total_interactions: int = Field(..., description="Total interactions at snapshot time")
    avg_success_rate: Optional[float] = Field(None, description="Average success rate")
    snapshot_data: Dict[str, Any] = Field(..., description="Snapshot data")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
