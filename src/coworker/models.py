from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


class McpServer(BaseModel):
    name: str
    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    enabled: bool = True


class Skill(BaseModel):
    name: str
    path: str
    description: str = ""
    enabled: bool = True


class Permissions(BaseModel):
    allow: list[str] = Field(default_factory=list)
    deny: list[str] = Field(default_factory=list)


class ClaudeOverrides(BaseModel):
    effortLevel: str = "medium"
    skipDangerousModePermissionPrompt: bool = False
    extra: dict[str, Any] = Field(default_factory=dict)


class GeminiOverrides(BaseModel):
    extra: dict[str, Any] = Field(default_factory=dict)


class OpenCodeOverrides(BaseModel):
    extra: dict[str, Any] = Field(default_factory=dict)


class CoworkerConfig(BaseModel):
    version: str = "1"
    scope: str = "global"  # global | project

    mcp: list[McpServer] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    permissions: Permissions = Field(default_factory=Permissions)

    # tool-specific overrides
    claude: ClaudeOverrides = Field(default_factory=ClaudeOverrides)
    gemini: GeminiOverrides = Field(default_factory=GeminiOverrides)
    opencode: OpenCodeOverrides = Field(default_factory=OpenCodeOverrides)
