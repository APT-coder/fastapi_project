from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import attributes
from app.models.audit_mixin import AuditMixin


@event.listens_for(Session, "before_flush")
def apply_audit_fields(session, flush_context, instances):
    user_id = session.info.get("current_user_id")

    if user_id is None:
        return  # no user info available, skip

    for obj in session.new:
        if isinstance(obj, AuditMixin):
            obj.created_by = user_id
            obj.updated_by = user_id

    for obj in session.dirty:
        if isinstance(obj, AuditMixin):
            obj.updated_by = user_id
            attributes.flag_modified(obj, "updated_by")
