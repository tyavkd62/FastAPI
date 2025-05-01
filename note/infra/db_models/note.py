from database import Base
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

'''
노트와 태그의 다대다 관계 설정 테이블'''
note_tag_association = Table(
    'Note_Tag',
    Base.metadata,
    Column('note_id', String(36), ForeignKey('Note.id')),
    Column('tag_id', String(36), ForeignKey('Tag.id')),
)

class Note(Base):
    __tablename__ = 'Note'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    '''
    다대다 관계 설정'''
    tags = relationship(
        'Tag',
        secondary=note_tag_association,
        back_populates='notes', # 노트 객체를 가져올 때 관련 태그를 모두 로드
        lazy='joined'
    )

class Tag(Base):
    __tablename__ = 'Tag'
    
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    '''
    다대다 관계 설정'''
    notes = relationship(
        'Note',
        secondary=note_tag_association,
        back_populates='tags',
        lazy='joined'
    )