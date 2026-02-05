"""
File: database_service.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.agent import Agent
from app.db.models.prompt import Prompt
from app.db.models.role import Role
from app.db.models.user import User
from app.schemas.db.agent import AgentCreate, AgentUpdate
from app.schemas.db.prompt import PromptCreate, PromptUpdate
from app.schemas.db.role import RoleCreate, RoleUpdate
from app.schemas.db.user import UserCreate, UserUpdate
from app.utils.password import hash_password

T = TypeVar("T")


class DatabaseService:
    """
    High-level service over database CRUD operations.

    Uses Session and Pydantic schemas to persist agents and prompts in
    Postgres. Each agent has at most one prompt (prompt_id).
    """

    def __init__(self, session: Session) -> None:
        """Store the database session for CRUD operations.

        Args:
            session (Session): SQLAlchemy session bound to the request.
        """
        self._session = session

    def _update_object(self, instance: T, data: BaseModel) -> T:
        """Set on instance only attributes that were explicitly set in data.

        Args:
            instance (T): ORM model instance to update.
            data (BaseModel): Pydantic update schema (only set fields applied).

        Returns:
            T: The same instance with attributes updated.
        """
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        return instance

    # --- Agents ---
    def create_agent(self, data: AgentCreate) -> Agent:
        """Create and persist a new agent.

        Args:
            data (AgentCreate): Name, config, and optional prompt_id.

        Returns:
            Agent: The created agent with id and timestamps.
        """
        agent = Agent(
            name=data.name,
            config=data.config,
            prompt_id=data.prompt_id,
        )
        self._session.add(agent)
        self._session.flush()
        return agent

    def get_agent(self, id: int) -> Agent | None:
        """Fetch an agent by primary key.

        Args:
            id (int): Agent primary key.

        Returns:
            Agent | None: The agent if found, else None.
        """
        return self._session.get(Agent, id)

    def list_agents(self, *, skip: int = 0, limit: int = 100) -> list[Agent]:
        """List agents with optional pagination.

        Args:
            skip (int): Number of records to skip. Defaults to 0.
            limit (int): Max records to return. Defaults to 100.

        Returns:
            list[Agent]: List of agents ordered by id.
        """
        stmt = select(Agent).offset(skip).limit(limit).order_by(Agent.id)
        return list(self._session.scalars(stmt).all())

    def update_agent(self, id: int, data: AgentUpdate) -> Agent | None:
        """Update an agent by id with only the provided fields.

        Args:
            id (int): Agent primary key.
            data (AgentUpdate): Fields to update (only set fields applied).

        Returns:
            Agent | None: The updated agent if found, else None.
        """
        agent = self.get_agent(id)
        if agent is None:
            return None
        self._update_object(agent, data)
        self._session.flush()
        return agent

    def delete_agent(self, id: int) -> bool:
        """Delete an agent by id.

        Args:
            id (int): Agent primary key.

        Returns:
            bool: True if deleted, False if not found.
        """
        agent = self.get_agent(id)
        if agent is None:
            return False
        self._session.delete(agent)
        return True

    # --- Prompts ---
    def create_prompt(self, data: PromptCreate) -> Prompt:
        """Create and persist a new prompt.

        Args:
            data (PromptCreate): Name, content, and optional variables.

        Returns:
            Prompt: The created prompt with id and timestamps.
        """
        prompt = Prompt(
            name=data.name,
            content=data.content,
            variables=data.variables,
        )
        self._session.add(prompt)
        self._session.flush()
        return prompt

    def get_prompt(self, id: int) -> Prompt | None:
        """Fetch a prompt by primary key.

        Args:
            id (int): Prompt primary key.

        Returns:
            Prompt | None: The prompt if found, else None.
        """
        return self._session.get(Prompt, id)

    def list_prompts(self, *, skip: int = 0, limit: int = 100) -> list[Prompt]:
        """List prompts with optional pagination.

        Args:
            skip (int): Number of records to skip. Defaults to 0.
            limit (int): Max records to return. Defaults to 100.

        Returns:
            list[Prompt]: List of prompts ordered by id.
        """
        stmt = select(Prompt).offset(skip).limit(limit).order_by(Prompt.id)
        return list(self._session.scalars(stmt).all())

    def update_prompt(self, id: int, data: PromptUpdate) -> Prompt | None:
        """Update a prompt by id with only the provided fields.

        Args:
            id (int): Prompt primary key.
            data (PromptUpdate): Fields to update (only set fields applied).

        Returns:
            Prompt | None: The updated prompt if found, else None.
        """
        prompt = self.get_prompt(id)
        if prompt is None:
            return None
        self._update_object(prompt, data)
        self._session.flush()
        return prompt

    def delete_prompt(self, id: int) -> bool:
        """Delete a prompt by id.

        Args:
            id (int): Prompt primary key.

        Returns:
            bool: True if deleted, False if not found.
        """
        prompt = self.get_prompt(id)
        if prompt is None:
            return False
        self._session.delete(prompt)
        return True

    # --- Users ---
    def create_user(self, data: UserCreate) -> User:
        """Create and persist a new user (password is hashed).

        Args:
            data (UserCreate): Email, username, full_name, password, is_active.

        Returns:
            User: The created user with id and timestamps.
        """
        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            is_active=data.is_active,
        )
        self._session.add(user)
        self._session.flush()
        return user

    def get_user(self, id: int) -> User | None:
        """Fetch a user by primary key.

        Args:
            id (int): User primary key.

        Returns:
            User | None: The user if found, else None.
        """
        return self._session.get(User, id)

    def list_users(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        """List users with optional pagination.

        Args:
            skip (int): Number of records to skip. Defaults to 0.
            limit (int): Max records to return. Defaults to 100.

        Returns:
            list[User]: List of users ordered by id.
        """
        stmt = select(User).offset(skip).limit(limit).order_by(User.id)
        return list(self._session.scalars(stmt).all())

    def update_user(self, id: int, data: UserUpdate) -> User | None:
        """Update a user by id with only the provided fields.

        Args:
            id (int): User primary key.
            data (UserUpdate): Fields to update (only set fields applied).

        Returns:
            User | None: The updated user if found, else None.
        """
        user = self.get_user(id)
        if user is None:
            return None
        dump = data.model_dump(exclude_unset=True)
        if "password" in dump:
            user.hashed_password = hash_password(dump.pop("password"))
        for key, value in dump.items():
            setattr(user, key, value)
        self._session.flush()
        return user

    def delete_user(self, id: int) -> bool:
        """Delete a user by id.

        Args:
            id (int): User primary key.

        Returns:
            bool: True if deleted, False if not found.
        """
        user = self.get_user(id)
        if user is None:
            return False
        self._session.delete(user)
        return True

    # --- Roles ---
    def create_role(self, data: RoleCreate) -> Role:
        """Create and persist a new role.

        Args:
            data (RoleCreate): Name and optional description.

        Returns:
            Role: The created role with id and timestamps.
        """
        role = Role(name=data.name, description=data.description)
        self._session.add(role)
        self._session.flush()
        return role

    def get_role(self, id: int) -> Role | None:
        """Fetch a role by primary key.

        Args:
            id (int): Role primary key.

        Returns:
            Role | None: The role if found, else None.
        """
        return self._session.get(Role, id)

    def list_roles(self, *, skip: int = 0, limit: int = 100) -> list[Role]:
        """List roles with optional pagination.

        Args:
            skip (int): Number of records to skip. Defaults to 0.
            limit (int): Max records to return. Defaults to 100.

        Returns:
            list[Role]: List of roles ordered by id.
        """
        stmt = select(Role).offset(skip).limit(limit).order_by(Role.id)
        return list(self._session.scalars(stmt).all())

    def update_role(self, id: int, data: RoleUpdate) -> Role | None:
        """Update a role by id with only the provided fields.

        Args:
            id (int): Role primary key.
            data (RoleUpdate): Fields to update (only set fields applied).

        Returns:
            Role | None: The updated role if found, else None.
        """
        role = self.get_role(id)
        if role is None:
            return None
        self._update_object(role, data)
        self._session.flush()
        return role

    def delete_role(self, id: int) -> bool:
        """Delete a role by id.

        Args:
            id (int): Role primary key.

        Returns:
            bool: True if deleted, False if not found.
        """
        role = self.get_role(id)
        if role is None:
            return False
        self._session.delete(role)
        return True

    # --- User-Role relationship ---
    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """Assign a role to a user (idempotent: no-op if already assigned).

        Args:
            user_id (int): User primary key.
            role_id (int): Role primary key.

        Returns:
            bool: True if user and role exist; False if either not found.
        """
        user = self.get_user(user_id)
        role = self.get_role(role_id)
        if user is None or role is None:
            return False
        if role not in user.roles:
            user.roles.append(role)
        return True

    def remove_role_from_user(self, user_id: int, role_id: int) -> bool:
        """Remove a role from a user.

        Args:
            user_id (int): User primary key.
            role_id (int): Role primary key.

        Returns:
            bool: True if the assignment existed and was removed;
                False otherwise.
        """
        user = self.get_user(user_id)
        role = self.get_role(role_id)
        if user is None or role is None:
            return False
        if role in user.roles:
            user.roles.remove(role)
            return True
        return False

    def list_roles_for_user(self, user_id: int) -> list[Role]:
        """List all roles assigned to a user.

        Args:
            user_id (int): User primary key.

        Returns:
            list[Role]: List of roles for the user; empty if user not found.
        """
        user = self.get_user(user_id)
        if user is None:
            return []
        return list(user.roles)
