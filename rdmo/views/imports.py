from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper

from .models import View
from .validators import ViewLockedValidator, ViewUniqueURIValidator

import_helper_view = ElementImportHelper(
    model=View,
    model_path="views.view",
    validators=(ViewLockedValidator, ViewUniqueURIValidator),
    lang_fields=('help', 'title'),
    extra_fields=(
        ExtraFieldHelper(field_name='order'),
        ExtraFieldHelper(field_name='template'),
        ExtraFieldHelper(field_name='available', value=True),
    ),
    m2m_instance_fields=('catalogs',),
)
