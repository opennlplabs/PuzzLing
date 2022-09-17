const dropdownContainer = document.querySelector(".nav-item .dropdown-menu");

const languages = ['Assamese','Bengali',	'Gujarati',
'Hindi',		'Kannada',		'Malayalam',
'Marathi',		'Nepali',		'Odia (Oriya)',	
'Punjabi',		'Sindhi',	'Sinhala (Sinhalese)', 
'Tamil',	'Telugu',	'Urdu',

'Burmese (Myanmar)',		'Cebuano',	'Dhivehi',
'Hmong',	'Indonesian',	'Javanese',
'Khmer',	'Malay', 'Loa',
'Sundanese',	'Tagalog (Filipino)',	'Thai',
'Urdu',	'Vietnamese',

'Arabic', 'Hebrew',	'Pashto',
'Persian',	'Uighur',	'Turkmen',

'Armenian', 'Azerbaijani',	'Chinese (Simplified)',
'Chinese (Traditional)',	'Georgian',	'Japanese',
'Kazakh',	'Kirghiz',	'Korean',
'Kurdish',	'Kyrgyz',	'Mongolian',
'Russian',	'Tagalog',	'Tajik',
'Tatar',	'Uzbek',

'Afrikaans',	'Amharic',	'Bambara',
'English',	'French',	'Hausa',
'Igbo',	'Kinyarwanda',	'Lingala',
'Malagasy',	'Nyanja (Chichewa)',	'Oromo',
'Sesotho','Shona',	'Somali',
'Swahili', 'Tigrinya', 'Tsonga',
'Twi',	'Xhosa',	'Yoruba',
'Zulu',

'Albanian',	'Aragonese',	'Bashkir',
'Basque',	'Belarusian',	'Bosnian'	,
'Breton',	'Bulgarian',	'Catalan',
'Chechen',	'Chuvash',	'Corsican',
'Croatian',	'Czech',	'Danish',
'Dutch',	'English',	'Esperanto',
'Estonian',	'Finnish',	'French',
'Frisian',	'Galician',	'German',
'Greek',	'Hungarian',	'Icelandic',
'Irish',	'Italian',	'Latin',
'Latvian',	'Lithuanian',	'Luxembourgish',
'Macedonian',	'Maltese',	'Norwegian Bokmål',
'Occitan',	'Polish',	'Portuguese',
'Romanian',	'Scots Gaelic',	'Serbian',
'Slovak',	'Slovenian',	'Spanish',
'Swedish',	'Turkish',	'Ukrainian',
'Welsh',	'Yiddish',

'Aymara',	'Dutch',	'English',
'French',	'Guarani',	'Haitian',
'Hawaiian',	'Portuguese',	'Quechua',
'Samoan', 'Spanish',	'Yiddish',

'Maori']

languages.sort()
languages.forEach(language => {
dropdownContainer.innerHTML += `<a class="dropdown-item" href="?language=${language}">${language}</a>`
})