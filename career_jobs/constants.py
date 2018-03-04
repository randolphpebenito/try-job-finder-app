COUNTRY_MALAYSIA = 'my'
COUNTRY_SINGAPORE = 'sg'
COUNTRY_PHILIPPINES = 'ph'
COUNTRY_THAILAND = 'th'

COUNTRY_CHOICES = (
    (COUNTRY_MALAYSIA, 'Malaysia'),
    (COUNTRY_SINGAPORE, 'Singapore'),
    (COUNTRY_PHILIPPINES, 'Philippines'),
    (COUNTRY_THAILAND, 'Thailand'),
)

JOB_FULL_TIME = 'ft'
JOB_PART_TIME = 'pt'

JOB_TYPE_CHOICES = (
    (JOB_FULL_TIME, 'Full Time'),
    (JOB_PART_TIME, 'Part Time'),
)

JOB_STATUS_AVAILABLE = 'op'
JOB_STATUS_NOT_AVAILABLE = 'cl'

JOB_STATUS_CHOICES = (
    (JOB_STATUS_AVAILABLE, 'Open'),
    (JOB_STATUS_NOT_AVAILABLE, 'Closed'),
)
