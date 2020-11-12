"""
Prototype PBLL Project Metadata Schema

BASE (These descriptors are defined for the model: ProjectPrototype)
--------

    title
    creator
    origin
    description
    publisher
    publish_date
    contributors
    rights
    uri

EXTENDED (These descriptors are defined here, as a metadata schema for ProjectPrototype's)
--------
    subject
    language

    WORLD READINESS STANDARD (wr)
    wr_goal_area.communication
    wr_goal_area.cultures
    wr_goal_area.connections
    wr_goal_area.comparisons
    wr_goal_area.communities

    21ST CENTURY SKILLS (cs)
    cs_interdisciplinary_themes
    cs_info_media_technology_skills
    cs_like_career_skills

    INSTRUCTIONAL_CONTEXT (ic)
    ic_heritage_learners
    ic_target_audience.description
    ic_target_audience.role
    ic_target_audience.location
    ic_product.description
    ic_product.target_culture

    LANGUAGE_PROFICIENCY (lp)
    lp_actfl_scale
    lp_ilr_scale.listening
    lp_ilr_scale.reading
    lp_ilr_scale.speaking
    lp_ilr_scale.writing
"""

"""
The following tuples are used by reposite.models.PrototypeMetaElement 
to enforce the definition of metadata types and categories. New metadata 
definitions and or categories should be added to these tuples to ensure
they are enforced in the PrototypeMetaElement model and relevant table.

Format: <metadata identifier>, <metadata display string>

Note: each of the types listed below must have a corresponding form definition
added to PrototypeMetadataForm defined in this file. This ensures that the relative
form used to create metadata elements are properly associated. 

Additionally, a controlled vocabulary may be defined for each metatdata form to constrain the data. 
"""

from collections import OrderedDict, namedtuple

MetaElementDef = namedtuple('MetaElementDef', 'id id_display category category_display')

CATEGORY_DEFINITIONS = OrderedDict()
CATEGORY_DEFINITIONS['subject'] = 'Subject Area'
CATEGORY_DEFINITIONS['language'] = 'Language'
CATEGORY_DEFINITIONS['instructional_context'] = 'Instructional Context'
CATEGORY_DEFINITIONS['language_proficiency'] = 'Language Proficiency'
CATEGORY_DEFINITIONS['world_readiness'] = 'World Readiness Standards'
CATEGORY_DEFINITIONS['21st_century_skills'] = '21st Century Skills'


METADATA = (
    MetaElementDef(
        id='subject',
        id_display='Subject Area(s)',
        category='subject',
        category_display=CATEGORY_DEFINITIONS['subject']), 
    MetaElementDef(
        id='language',
        id_display='Language(s)',
        category='language',
        category_display=CATEGORY_DEFINITIONS['language']), 
    MetaElementDef(
        id='ic_heritage_learners',
        id_display='Heritage Learners',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='ic_target_audience_description',
        id_display='Target Audience Description',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='ic_target_audience_role',
        id_display='Audience Role',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='ic_target_audience_location',
        id_display='Audience Location',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='ic_product_description',
        id_display='Product Description',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='ic_product_target_culture',
        id_display='Product Target Culture',
        category='instructional_context',
        category_display=CATEGORY_DEFINITIONS['instructional_context']), 
    MetaElementDef(
        id='lp_actfl_scale',
        id_display='ACTFL Scale',
        category='language_proficiency',
        category_display=CATEGORY_DEFINITIONS['language_proficiency']), 
    MetaElementDef(
        id='lp_ilr_scale_listening',
        id_display='ILR Scale Listening',
        category='language_proficiency',
        category_display=CATEGORY_DEFINITIONS['language_proficiency']), 
    MetaElementDef(
        id='lp_ilr_scale_reading',
        id_display='ILR Scale Reading',
        category='language_proficiency',
        category_display=CATEGORY_DEFINITIONS['language_proficiency']), 
    MetaElementDef(
        id='lp_ilr_scale_speaking',
        id_display='ILR Scale Speaking',
        category='language_proficiency',
        category_display=CATEGORY_DEFINITIONS['language_proficiency']), 
    MetaElementDef(
        id='lp_ilr_scale_writing',
        id_display='ILR Scale Writing',
        category='language_proficiency',
        category_display=CATEGORY_DEFINITIONS['language_proficiency']), 
    MetaElementDef(
        id='wr_goal_area_communication',
        id_display='Communication',
        category='world_readiness',
        category_display=CATEGORY_DEFINITIONS['world_readiness']), 
    MetaElementDef(
        id='wr_goal_area_cultures',
        id_display='Cultures',
        category='world_readiness',
        category_display=CATEGORY_DEFINITIONS['world_readiness']), 
    MetaElementDef(
        id='wr_goal_area_connections',
        id_display='Connections',
        category='world_readiness',
        category_display=CATEGORY_DEFINITIONS['world_readiness']), 
    MetaElementDef(
        id='wr_goal_area_comparisons',
        id_display='Comparisons',
        category='world_readiness',
        category_display=CATEGORY_DEFINITIONS['world_readiness']), 
    MetaElementDef(
        id='wr_goal_area_communities',
        id_display='Communities',
        category='world_readiness',
        category_display=CATEGORY_DEFINITIONS['world_readiness']), 
    MetaElementDef(
        id='cs_interdisciplinary_themes',
        id_display='Interdisciplinary Themes',
        category='21st_century_skills',
        category_display=CATEGORY_DEFINITIONS['21st_century_skills']), 
    MetaElementDef(
        id='cs_info_media_technology_skills',
        id_display='Information, Media, and Technology Skills',
        category='21st_century_skills',
        category_display=CATEGORY_DEFINITIONS['21st_century_skills']), 
    MetaElementDef(
        id='cs_like_career_skills',
        id_display='Life and Career Skills',
        category='21st_century_skills',
        category_display=CATEGORY_DEFINITIONS['21st_century_skills']),
)


METADATA_CATEGORIES             = tuple([(k, v) for k, v in CATEGORY_DEFINITIONS.items()])

METADATA_TYPES                  = tuple([(m.id, m.id_display) for m in METADATA])

METADATA_TYPES_TO_CATEGORIES    = {m.id: m.category for m in METADATA}

def meta_lookup(element_identifier=None):
    for e in METADATA:
        if e.id == element_identifier:
            return e
    return None

"""
CONTROLLED VOCABULARLY FOR BASE AND EXTENDED DESCRIPTORS
--------
"""

SUBJECT_AREAS = (
    ('architecture', 'architecture'),
    ('beauty', 'beauty'),
    ('communities', 'communities'),
    ('creativity', 'creativity'),
    ('design', 'design'),
    ('economy', 'economy'),
    ('education', 'education'),
    ('emigration/immigration', 'emigration/immigration'),
    ('entertainment', 'entertainment'),
    ('ethics', 'ethics'),
    ('ethnic identity', 'ethnic identity'),
    ('family', 'family'),
    ('fashion', 'fashion'),
    ('food', 'food'),
    ('friendship', 'friendship'),
    ('geography', 'geography'),
    ('global challenges', 'global challenges'),
    ('health', 'health'),
    ('heroes', 'heroes'),
    ('history', 'history'),
    ('language and literature', 'language and literature'),
    ('lifestyles', 'lifestyles'),
    ('national identity', 'national identity'),
    ('nature', 'nature'),
    ('philosophy', 'philosophy'),
    ('psychology', 'psychology'),
    ('restaurant', 'restaurant'),
    ('science', 'science'),
    ('social networks', 'social networks'),
    ('society', 'society'),
    ('sustainability', 'sustainability'),
    ('technology', 'technology'),
    ('the environment', 'the environment'),
    ('theater', 'theater'),
    ('traditions', 'traditions'),
    ('translation', 'translation'),
    ('travel', 'travel'),
    ('values', 'values'),
    ('visual arts', 'visual arts')
)

COPYRIGHT_TYPES = (
    ('http://creativecommons.org/', 'Creative Commons'),
)

WR_GOAL_AREA = {
    'communication': (
        ('Interpersonal', 'Interpersonal'),
        ('Interpretive', 'Interpretive'),
        ('Presentational', 'Presentational')
    ),

    'cultures': (
        ('Relating Cultural Practices to Perspectives',
         'Relating Cultural Practices to Perspectives'),
        ('Relating Cultural Products to Perspectives',
         'Relating Cultural Products to Perspectives')
    ),

    'connections': (
        ('Making Connections', 'Making Connections'),
        ('Acquiring Information and Diverse Perspectives',
         'Acquiring Information and Diverse Perspectives')
    ),

    'comparisons': (
        ('Language comparisons', 'Language comparisons'),
        ('Cultural comparisons', 'Cultural comparisons')
    ),

    'communities': (
        ('School and Global', 'School and Global'),
        ('Lifelong Learning', 'Lifelong Learning')
    )
}

CENTURY_SKILLS = {
    'interdisciplinary-themes': (
        ('Global Awareness', 'Global Awareness'),
        ('Civic Literacy', 'Civic Literacy'),
        ('Health Literacy', 'Health Literacy'),
        ('Financial, Economic, Business and Entrepreneurial Literacy',
         'Financial, Economic, Business and Entrepreneurial Literacy')
    ),

    'information-media-technology-skills': (
        ('Communication', 'Communication'),
        ('Collaboration', 'Collaboration'),
        ('Creativity and Innovation', 'Creativity and Innovation'),
        ('Information Literacy', 'Information Literacy'),
        ('Media Literacy', 'Media Literacy'),
        ('Technology Literacy', 'Technology Literacy'),
    ),

    'like-career-skills': (
        ('Flexibility and adaptability', 'Flexibility and adaptability'),
        ('Initiative and Self-Direction', 'Initiative and Self-Direction'),
        ('Social and Cross Cultural Skills',
         'Social and Cross Cultural Skills'),
        ('Productivity and Accountability', 'Productivity and Accountability'),
        ('Leadership and responsibility', 'Leadership and responsibility'),
    )
}

INSTRUCTIONAL_CONTEXTS = {
    'heritage-learners': (
        ('yes', 'Yes'),
        ('mixed', 'Mixed'),
        ('no', 'No')
    )
}

LANGUAGE_PROFICIENCY = {
    'actfl': (
        ('1', 'Novice Low'),
        ('2', 'Novice Mid'),
        ('3', 'Novice High'),
        ('4', 'Intermediate Low'),
        ('5', 'Intermediate Mid'),
        ('6', 'Intermediate High'),
        ('7', 'Advanced Low'),
        ('8', 'Advanced Mid'),
        ('9', 'Advanced High'),
        ('10', 'Superior')
    ),

    'ilr-reading': (
        ('0', 'Reading 0'),
        ('1', 'Reading 1'),
        ('2', 'Reading 2'),
        ('3', 'Reading 3'),
        ('4', 'Reading 4'),
        ('5', 'Reading 5')
    ),

    'ilr-listening': (
        ('0', 'Listening 0'),
        ('1', 'Listening 1'),
        ('2', 'Listening 2'),
        ('3', 'Listening 3'),
        ('4', 'Listening 4'),
        ('5', 'Listening 5')
    ),

    'ilr-speaking': (
        ('0', 'Speaking 0'),
        ('1', 'Speaking 1'),
        ('2', 'Speaking 2'),
        ('3', 'Speaking 3'),
        ('4', 'Speaking 4'),
        ('5', 'Speaking 5')
    ),

    'ilr-writing': (
        ('0', 'Writing 0'),
        ('1', 'Writing 1'),
        ('2', 'Writing 2'),
        ('3', 'Writing 3'),
        ('4', 'Writing 4'),
        ('5', 'Writing 5')
    )
}

LANGUAGES_NISO = [('All Languages', 'All Languages'), ('Achenese', 'Achenese'), ('Acoli', 'Acoli'), ('Adangme', 'Adangme'), ('Afrihili (Artificial language)', 'Afrihili (Artificial language)'), ('Afrikaans', 'Afrikaans'), ('Afro-Asiatic (Other)', 'Afro-Asiatic (Other)'), ('Akkadian', 'Akkadian'), ('Albanian', 'Albanian'), ('Aleut', 'Aleut'), ('Algonquian languages', 'Algonquian languages'), ('Aljamia', 'Aljamia'), ('Altaic (Other)', 'Altaic (Other)'), ('American Sign Language', 'American Sign Language'), ('Amharic', 'Amharic'), ('Apache languages', 'Apache languages'), ('Arabic', 'Arabic'), ('Aramaic', 'Aramaic'), ('Arapaho', 'Arapaho'), ('Araucanian', 'Araucanian'), ('Arawak', 'Arawak'), ('Armenian', 'Armenian'), ('Artificial (Other)', 'Artificial (Other)'), ('Assamese', 'Assamese'), ('Athapascan languages', 'Athapascan languages'), ('Austronesian (Other)', 'Austronesian (Other)'), ('Avaric', 'Avaric'), ('Avestan', 'Avestan'), ('Awadhi', 'Awadhi'), ('Aymara', 'Aymara'), ('Azerbaijani', 'Azerbaijani'), ('Aztec', 'Aztec'), ('Balinese', 'Balinese'), ('Baltic (Other)', 'Baltic (Other)'), ('Baluchi', 'Baluchi'), ('Bambara', 'Bambara'), ('Bamileke languages', 'Bamileke languages'), ('Banda', 'Banda'), ('Basa', 'Basa'), ('Bashkir', 'Bashkir'), ('Basque', 'Basque'), ('Beja', 'Beja'), ('Bemba', 'Bemba'), ('Bengali', 'Bengali'), ('Berber languages', 'Berber languages'), ('Bhojpuri', 'Bhojpuri'), ('Bikol', 'Bikol'), ('Bini', 'Bini'), ('Braj', 'Braj'), ('Breton', 'Breton'), ('Buginese', 'Buginese'), ('Bulgarian', 'Bulgarian'), ('Burmese', 'Burmese'), ('Byelorussian', 'Byelorussian'), ('Caddo', 'Caddo'), ('Carib', 'Carib'), ('Catalan', 'Catalan'), ('Caucasian (Other)', 'Caucasian (Other)'), ('Cebuano', 'Cebuano'), ('Celtic languages', 'Celtic languages'), ('Central American Indian (Other)', 'Central American Indian (Other)'), ('Chagatai', 'Chagatai'), ('Chamorro', 'Chamorro'), ('Chechen', 'Chechen'), ('Cherokee', 'Cherokee'), ('Cheyenne', 'Cheyenne'), ('Chibcha', 'Chibcha'), ('Chinese', 'Chinese'), ('Chinook jargon', 'Chinook jargon'), ('Choctaw', 'Choctaw'), ('Church Slavic', 'Church Slavic'), ('Chuvash', 'Chuvash'), ('Coptic', 'Coptic'), ('Cornish', 'Cornish'), ('Cree', 'Cree'), ('Creek', 'Creek'), ('Creoles and Pidgins (Other)', 'Creoles and Pidgins (Other)'), ('Creoles and Pidgins, English-based (Other)', 'Creoles and Pidgins, English-based (Other)'), ('Creoles and Pidgins, French-based (Other)', 'Creoles and Pidgins, French-based (Other)'), ('Creoles and Pidgins, Portuguese-based (Other)', 'Creoles and Pidgins, Portuguese-based (Other)'), ('Cushitic (Other)', 'Cushitic (Other)'), ('Czech', 'Czech'), ('Dakota', 'Dakota'), ('Danish', 'Danish'), ('Delaware', 'Delaware'), ('Dinka', 'Dinka'), ('Dogri', 'Dogri'), ('Dravidian (Other)', 'Dravidian (Other)'), ('Duala', 'Duala'), ('Dutch', 'Dutch'), ('Dutch, Middle (ca. 1050-1350)', 'Dutch, Middle (ca. 1050-1350)'), ('Dyula', 'Dyula'), ('Efik', 'Efik'), ('Egyptian', 'Egyptian'), ('Ekajuk', 'Ekajuk'), ('Elamite', 'Elamite'), ('English', 'English'), ('English', 'English'), ('English, Middle (1100-1500)', 'English, Middle (1100-1500)'), ('Eskimo', 'Eskimo'), ('Esperanto', 'Esperanto'), ('Estonian', 'Estonian'), ('Ethiopic', 'Ethiopic'), ('Ewe', 'Ewe'), ('Ewondo', 'Ewondo'), ('Fang', 'Fang'), ('Fanti', 'Fanti'), ('Faroese', 'Faroese'), ('Fijian', 'Fijian'), ('Finnish', 'Finnish'), ('Finno-Ugrian (Other)', 'Finno-Ugrian (Other)'), ('Fon', 'Fon'), ('French', 'French'), ('French, Middle (ca. 1400-1600)', 'French, Middle (ca. 1400-1600)'), ('French, Old (ca. 842-1400)', 'French, Old (ca. 842-1400)'), ('Friesian', 'Friesian'), ('Fula', 'Fula'), ('Gaelic (Scots)', 'Gaelic (Scots)'), ('Gallegan', 'Gallegan'), ('Ganda', 'Ganda'), ('Gayo', 'Gayo'), ('Georgian', 'Georgian'), ('German', 'German'), ('German, Middle High (ca. 1050-1500)', 'German, Middle High (ca. 1050-1500)'), ('German, Old High (ca. 750-1050)', 'German, Old High (ca. 750-1050)'), ('Germanic (Other)', 'Germanic (Other)'), ('Gilbertese', 'Gilbertese'), ('Gondi', 'Gondi'), ('Gothic', 'Gothic'), ('Grebo', 'Grebo'), ('Greek, Ancient (to 1453)', 'Greek, Ancient (to 1453)'), ('Greek, Modern (1453- )', 'Greek, Modern (1453- )'), ('Guarani', 'Guarani'), ('Gujarati', 'Gujarati'), ('G\xc3\xbe', 'G\xc3\xbe'), ('Haida', 'Haida'), ('Hausa', 'Hausa'), ('Hawaiian', 'Hawaiian'), ('Hebrew', 'Hebrew'), ('Herero', 'Herero'), ('Hiligaynon', 'Hiligaynon'), ('Himachali', 'Himachali'), ('Hindi', 'Hindi'), ('Hiri Motu', 'Hiri Motu'), ('Hungarian', 'Hungarian'), ('Hupa', 'Hupa'), ('Iban', 'Iban'), ('Icelandic', 'Icelandic'), ('Igbo', 'Igbo'), ('Ijo', 'Ijo'), ('Iloko', 'Iloko'), ('Indic (Other)', 'Indic (Other)'), ('Indo-European (Other)', 'Indo-European (Other)'), ('Indonesian', 'Indonesian'), ('Interlingua (International Auxiliary Language Association)', 'Interlingua (International Auxiliary Language Association)'), ('Iranian (Other)', 'Iranian (Other)'), ('Irish', 'Irish'), ('Iroquoian languages', 'Iroquoian languages'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Javanese', 'Javanese'), ('Judeo-Arabic', 'Judeo-Arabic'), ('Judeo-Persian', 'Judeo-Persian'), ('Kabyle', 'Kabyle'), ('Kachin', 'Kachin'), ('Kamba', 'Kamba'), ('Kannada', 'Kannada'), ('Kanuri', 'Kanuri'), ('Kara-Kalpak', 'Kara-Kalpak'), ('Karen', 'Karen'), ('Kashmiri', 'Kashmiri'), ('Kawi', 'Kawi'), ('Kazakh', 'Kazakh'), ('Khasi', 'Khasi'), ('Khmer', 'Khmer'), ('Khoisan (Other)', 'Khoisan (Other)'), ('Khotanese', 'Khotanese'), ('Kikuyu', 'Kikuyu'), ('Kinyarwanda', 'Kinyarwanda'), ('Kirghiz', 'Kirghiz'), ('Kongo', 'Kongo'), ('Konkani', 'Konkani'), ('Korean', 'Korean'), ('Kpelle', 'Kpelle'), ('Kru', 'Kru'), ('Kuanyama', 'Kuanyama'), ('Kurdish', 'Kurdish'), ('Kurukh', 'Kurukh'), ('Kusaie', 'Kusaie'), ('Kutenai', 'Kutenai'), ('Ladino', 'Ladino'), ('Lahnd', 'Lahnd'), ('Lamba', 'Lamba'), ('Langue d`oc (post-1500)', 'Langue d`oc (post-1500)'), ('Lao', 'Lao'), ('Lapp', 'Lapp'), ('Latin', 'Latin'), ('Latvian', 'Latvian'), ('Lingala', 'Lingala'), ('Lithuanian', 'Lithuanian'), ('Lozi', 'Lozi'), ('Luba-Katanga', 'Luba-Katanga'), ('Luiseno', 'Luiseno'), ('Lunda', 'Lunda'), ('Luo (Kenya and Tanzania)', 'Luo (Kenya and Tanzania)'), ('Macedonian', 'Macedonian'), ('Madurese', 'Madurese'), ('Magahi', 'Magahi'), ('Maithili', 'Maithili'), ('Makasar', 'Makasar'), ('Malagasy', 'Malagasy'), ('Malay', 'Malay'), ('Malayalam', 'Malayalam'), ('Maltese', 'Maltese'), ('Mandingo', 'Mandingo'), ('Manipuri', 'Manipuri'), ('Manobo languages', 'Manobo languages'), ('Manx', 'Manx'), ('Maori', 'Maori'), ('Marathi', 'Marathi'), ('Marshall', 'Marshall'), ('Marwari', 'Marwari'), ('Masai', 'Masai'), ('Mayan languages', 'Mayan languages'), ('Mende', 'Mende'), ('Micmac', 'Micmac'), ('Minangkabau', 'Minangkabau'), ('Miscellaneous (Other)', 'Miscellaneous (Other)'), ('Mohawk', 'Mohawk'), ('Moldavian', 'Moldavian'), ('Mon-Khmer (Other)', 'Mon-Khmer (Other)'), ('Mongo', 'Mongo'), ('Mongolian', 'Mongolian'), ('Mossi', 'Mossi'), ('Multiple languages', 'Multiple languages'), ('Munda (Other)', 'Munda (Other)'), ('Navajo', 'Navajo'), ('Ndebele (Zimbabwe)', 'Ndebele (Zimbabwe)'), ('Ndonga', 'Ndonga'), ('Nepali', 'Nepali'), ('Newari', 'Newari'), ('Niger-Kordofanian (Other)', 'Niger-Kordofanian (Other)'), ('Niuean', 'Niuean'), ('North American Indian (Other)', 'North American Indian (Other)'), ('Northern Sotho', 'Northern Sotho'), ('Norwegian', 'Norwegian'), ('Nubian languages', 'Nubian languages'), ('Nyamwezi', 'Nyamwezi'), ('Nyanja', 'Nyanja'), ('Nyankole', 'Nyankole'), ('Nyoro', 'Nyoro'), ('Nzima', 'Nzima'), ('Ojibwa', 'Ojibwa'), ('Old Persian (ca. 600-400 B.C.)', 'Old Persian (ca. 600-400 B.C.)'), ('Oriya', 'Oriya'), ('Oromo', 'Oromo'), ('Osage', 'Osage'), ('Ossetic', 'Ossetic'), ('Otomian languages', 'Otomian languages'), ('Pahlavi', 'Pahlavi'), ('Palauan', 'Palauan'), ('Pali', 'Pali'), ('Pampanga', 'Pampanga'), ('Pangasinan', 'Pangasinan'), ('Panjabi', 'Panjabi'), ('Papiamento', 'Papiamento'), ('Papuan-Australian (Other)', 'Papuan-Australian (Other)'), ('Persian', 'Persian'), ('Polish', 'Polish'), ('Ponape', 'Ponape'), ('Portuguese', 'Portuguese'), ('Prakrit languages', 'Prakrit languages'), ('Provencal, Old (to 1500)', 'Provencal, Old (to 1500)'), ('Pushto', 'Pushto'), ('Quechua', 'Quechua'), ('Raeto-Romance', 'Raeto-Romance'), ('Rajasthani', 'Rajasthani'), ('Rarotongan', 'Rarotongan'), ('Romance (Other)', 'Romance (Other)'), ('Romanian', 'Romanian'), ('Romany', 'Romany'), ('Rundi', 'Rundi'), ('Russian', 'Russian'), ('Salishan languages', 'Salishan languages'), ('Samaritan Aramaic', 'Samaritan Aramaic'), ('Samoan', 'Samoan'), ('Sandawe', 'Sandawe'), ('Sango', 'Sango'), ('Sanskrit', 'Sanskrit'), ('Scots', 'Scots'), ('Selkup', 'Selkup'), ('Semitic (Other)', 'Semitic (Other)'), ('Serbo-Croatian (Cyrillic)', 'Serbo-Croatian (Cyrillic)'), ('Serbo-Croatian (Roman)', 'Serbo-Croatian (Roman)'), ('Serer', 'Serer'), ('Shan', 'Shan'), ('Shona', 'Shona'), ('Sidamo', 'Sidamo'), ('Siksika', 'Siksika'), ('Sindhi', 'Sindhi'), ('Sinhalese', 'Sinhalese'), ('Sino-Tibetan (Other)', 'Sino-Tibetan (Other)'), ('Siouan languages', 'Siouan languages'), ('Slavic (Other)', 'Slavic (Other)'), ('Slovak', 'Slovak'), ('Slovenian', 'Slovenian'), ('Somali', 'Somali'), ('Songhai', 'Songhai'), ('Sorbian languages', 'Sorbian languages'), ('Sotho', 'Sotho'), ('South American Indian (Other)', 'South American Indian (Other)'), ('Spanish', 'Spanish'), ('Sukuma', 'Sukuma'), ('Sumerian', 'Sumerian'), ('Sundanese', 'Sundanese'), ('Susu', 'Susu'), ('Swahili', 'Swahili'), ('Swazi', 'Swazi'), ('Syriac', 'Syriac'), ('Tagalog', 'Tagalog'), ('Tahitian', 'Tahitian'), ('Tajik', 'Tajik'), ('Tamil', 'Tamil'), ('Tatar', 'Tatar'), ('Telugu', 'Telugu'), ('Tereno', 'Tereno'), ('Thai', 'Thai'), ('Tibetan', 'Tibetan'), ('Tigre', 'Tigre'), ('Tigrinya', 'Tigrinya'), ('Timne', 'Timne'), ('Tivi', 'Tivi'), ('Tlingit', 'Tlingit'), ('Tonga (Nyasa)', 'Tonga (Nyasa)'), ('Tonga (Tonga Islands)', 'Tonga (Tonga Islands)'), ('Truk', 'Truk'), ('Tsimshian', 'Tsimshian'), ('Tsonga', 'Tsonga'), ('Tswana', 'Tswana'), ('Tumbuka', 'Tumbuka'), ('Turkish', 'Turkish'), ('Turkish, Ottoman', 'Turkish, Ottoman'), ('Turkmen', 'Turkmen'), ('Twi', 'Twi'), ('Ugaritic', 'Ugaritic'), ('Uighur', 'Uighur'), ('Ukrainian', 'Ukrainian'), ('Umbundu', 'Umbundu'), ('Undetermined', 'Undetermined'), ('Urdu', 'Urdu'), ('Uzbek', 'Uzbek'), ('Vai', 'Vai'), ('Venda', 'Venda'), ('Vietnamese', 'Vietnamese'), ('Votic', 'Votic'), ('Wakashan languages', 'Wakashan languages'), ('Walamo', 'Walamo'), ('Waray', 'Waray'), ('Washo', 'Washo'), ('Welsh', 'Welsh'), ('Wolof', 'Wolof'), ('Xhosa', 'Xhosa'), ('Yao', 'Yao'), ('Yap', 'Yap'), ('Yiddish', 'Yiddish'), ('Yoruba', 'Yoruba'), ('Zapotec', 'Zapotec'), ('Zenaga', 'Zenaga'), ('Zulu', 'Zulu'), ('Zuni', 'Zuni')]


"""
PrototypeMetadataForm is designed to define form fields used in ProjectPrototype forms. See reposite.forms to understand
how these fields are used.

Note that the form fields defined below are based on the metadata schema illustrated above (and its related choices
or 'vocabulary'). If there are additions, deletions, or modifications to the
schema above, they need to be reflected and/or edited in the relevant form field definitions defined here.

Alert: the category attribute is required for each form widget. This should reflect one of the items in METADATA_CATEGORIES above.
"""

from django import forms

class PrototypeMetadataForm(forms.Form):
    default_input_size = '60'

    element = meta_lookup('subject')
    subject = forms.MultipleChoiceField(
        choices=SUBJECT_AREAS,
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        widget=forms.CheckboxSelectMultiple(attrs={'data_value': element.id}),
        required=True)

    element = meta_lookup('language')
    language = forms.MultipleChoiceField(
        choices=LANGUAGES_NISO,
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        widget=forms.CheckboxSelectMultiple(attrs={'data_value': element.id}),
        required=False)

    element = meta_lookup('ic_heritage_learners')
    ic_heritage_learners = forms.ChoiceField(
        choices=INSTRUCTIONAL_CONTEXTS['heritage-learners'],
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.RadioSelect(attrs={'class': ''}),
        required=False)

    element = meta_lookup('ic_target_audience_description')
    ic_target_audience_description = forms.CharField(
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False)

    element = meta_lookup('ic_target_audience_role')
    ic_target_audience_role = forms.CharField(
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    element = meta_lookup('ic_target_audience_location')
    ic_target_audience_location = forms.CharField(
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    element = meta_lookup('ic_product_description')
    ic_product_description = forms.CharField(
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False)

    element = meta_lookup('ic_product_target_culture')
    ic_product_target_culture = forms.CharField(
        label=element.category_display,
        label_suffix=element.id_display,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    element = meta_lookup('lp_actfl_scale')
    lp_actfl_scale = forms.MultipleChoiceField(
        choices=LANGUAGE_PROFICIENCY['actfl'],
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        required=False)

    element = meta_lookup('lp_ilr_scale_listening')
    lp_ilr_scale_listening = forms.MultipleChoiceField(
        choices=LANGUAGE_PROFICIENCY['ilr-listening'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('lp_ilr_scale_reading')
    lp_ilr_scale_reading = forms.MultipleChoiceField(
        choices=LANGUAGE_PROFICIENCY['ilr-reading'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('lp_ilr_scale_speaking')
    lp_ilr_scale_speaking = forms.MultipleChoiceField(
        choices=LANGUAGE_PROFICIENCY['ilr-speaking'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('lp_ilr_scale_writing')
    lp_ilr_scale_writing = forms.MultipleChoiceField(
        choices=LANGUAGE_PROFICIENCY['ilr-writing'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('wr_goal_area_communication')
    wr_goal_area_communication = forms.MultipleChoiceField(
        choices=WR_GOAL_AREA['communication'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('wr_goal_area_cultures')
    wr_goal_area_cultures = forms.MultipleChoiceField(
        choices=WR_GOAL_AREA['cultures'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('wr_goal_area_connections')
    wr_goal_area_connections = forms.MultipleChoiceField(
        choices=WR_GOAL_AREA['connections'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('wr_goal_area_comparisons')
    wr_goal_area_comparisons = forms.MultipleChoiceField(
        choices=WR_GOAL_AREA['comparisons'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('wr_goal_area_communities')
    wr_goal_area_communities = forms.MultipleChoiceField(
        choices=WR_GOAL_AREA['communities'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('cs_interdisciplinary_themes')
    cs_interdisciplinary_themes = forms.MultipleChoiceField(
        choices=CENTURY_SKILLS['interdisciplinary-themes'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('cs_info_media_technology_skills')
    cs_info_media_technology_skills = forms.MultipleChoiceField(
        choices=CENTURY_SKILLS['information-media-technology-skills'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    element = meta_lookup('cs_like_career_skills')
    cs_like_career_skills = forms.MultipleChoiceField(
        choices=CENTURY_SKILLS['like-career-skills'],
        widget=forms.CheckboxSelectMultiple(attrs={'class': '', 'data_value': element.id}),
        label=element.category_display,
        label_suffix=element.id_display,
        help_text='Check all that apply.',
        required=False)

    def multiple_choice_fields(self):
        return [field_name for field_name, field_type in self.fields.items() if type(field_type) == forms.MultipleChoiceField]

    
    def display_order_fields(self):
        """ Returns the definition order of the field names. """
        return self.fields.keys()


