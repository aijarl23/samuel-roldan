from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

GRUPOS_STAFF = {'Odontologo', 'Odontólogo', 'Auxiliar', 'Administrador'}


@receiver(m2m_changed, sender=User.groups.through)
def _marcar_staff_segun_grupo(sender, instance, action, pk_set, **kwargs):
    """El acceso de Odontólogo/Auxiliar a la edición completa de datos (EPS,
    antecedentes, acudiente, etc.) vive en /admin/, restringido por los
    permisos del grupo. Sin is_staff=True no pueden ni iniciar sesión ahí,
    aunque tengan el permiso — esto lo activa automáticamente al asignar
    el grupo, para no depender de que alguien recuerde marcar la casilla."""
    if action != 'post_add':
        return
    if isinstance(instance, User):
        if instance.groups.filter(name__in=GRUPOS_STAFF).exists() and not instance.is_staff:
            instance.is_staff = True
            instance.save(update_fields=['is_staff'])
