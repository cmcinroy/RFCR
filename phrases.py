#
# Define phrases for all languages
#
phrases = {
    'en': ('Hello', 'Goodbye', 
        'entered the class', 'left the class', 
        'absent for', 'present for', 
        'Please scan your card',
        'Reset system and exit (clear again to confirm)?',
        'Card {} is not registered for this class.',
        'Reading student data', ' done.',
        'WARNING: previous state is being used, but student data has changed.',
        '{} student(s) in class:',
        'Class is empty.',
        'Class is not empty.',
        'System state will be saved.',
        'Previous state found; system will be initialized from this prior state.',
        'ERROR: cannot save state.',
        'ERROR: cannot access previous state.',
        'ERROR: cannot remove previous state file.',
        'System has been reset to a clear initial state.',
        'days', 'hours', 'minutes', 'seconds'
        ),
    'fr': ('Bienvenue', 'Au revoir', 
        'a rejoint la classe', 'a quitté la classe', 
        'absent pendant', 'présent pendant', 
        'Veuillez analyser votre carte',
        'Réinitialiser le système et sortir (effacer à nouveau pour confirmer)?',
        'La carte {} n''est pas enregistrée pour cette classe.',
        'Traitement des données des élèves', ' fini.',
        'AVERTISSEMENT: l''état précédent est utilisé, mais le fichier de données a changé.',
        '{} Étudiant(s) dans la classe:',
        'La classe est vide.',
        'La classe n''est pas vide.',
        'L''état du système sera enregistré.',
        'Etat précédent trouvé; Système sera initialisé à partir de cet état antérieur.',
        'ERREUR: Impossible d''enregistrer l''état.',
        'ERREUR: impossible d''accéder à l''état précédent.',
        'ERREUR: impossible de supprimer le fichier d''état précédent.',
        'Le système a été réinitialisé à un état initial clair.',
        'jours', 'heures', 'minutes', 'secondes'
        )
}
PHRASE_ACTION = 2
PHRASE_DELTA = 4
PHRASE_INPUT = 6
PHRASE_RESET_CONFIRM = 7
PHRASE_NOTREG = 8
PHRASE_DATA_READ = 9
PHRASE_DATA_COMPLETE = 10
PHRASE_WARN_DATA_CHECK = 11
PHRASE_QUERY = 12
PHRASE_STATE_EMPTY = 13
PHRASE_STATE_NOT_EMPTY = 14
PHRASE_STATE_SAVE = 15
PHRASE_STATE_LOAD = 16
PHRASE_ERR_STATE_SAVE = 17
PHRASE_ERR_STATE_READ = 18
PHRASE_ERR_STATE_FILE = 19
PHRASE_RESET = 20
PHRASE_DAYS = 21
PHRASE_HRS = 22
PHRASE_MINS = 23
PHRASE_SECS = 24
