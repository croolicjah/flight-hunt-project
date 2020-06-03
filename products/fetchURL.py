from urllib.parse import urlparse
from urllib.parse import urlsplit
from urllib.parse import parse_qs
import requests
from psycopg2 import connect, OperationalError

airlines_iata = {'1A': ['Amadeus Global Travel Distribution', 'Hiszpania'], '1B': ['Abacus International', 'Singapur'],
                 '1C': ['EDS Information Business', 'Szwajcaria'], '1D': ['Radixx Solutions International', 'USA'],
                 '1E': ['Travelsky Technology', 'Chiny'], '1F': ['INFINI Travel Information', 'Japonia'],
                 '1G': ['Galileo International', 'USA'], '1H': ['Siren-Travel', 'Rosja'],
                 '1I': ['Netjets Aviation', 'Execjet', ' USA', ' Deutsche Rettungsflugwacht', 'Niemcy',
                        ' Nova Airlines', 'Navigator', ' Szwecja', ' Sky Trek International Airlines', 'Phazer', ' USA',
                        ' Sierra Nevada Airlines', 'USA', ' Pegasus Hava Tasimaciligi', 'Sunturk', ' Turcja'],
                 '1J': ['Axess international', 'Japonia'],
                 '1K': ['Sutra', 'linie lotnicze Sutra', 'USA', ' Southern Cross Distribution', 'Australia'],
                 '1L': ['Open Skies', 'USA'], '1M': ['JSC Transport Automated Information Systems', 'TAIS', 'Rosja'],
                 '1N': ['Navitaire', 'USA'], '1P': ['WorldSpan', 'USA'], '1Q': ['Sirena', 'Rosja'],
                 '1R': ['Hainan Phoenix Information Systems', 'Chiny'], '1S': ['CRS Sabre', 'USA'],
                 '1T': ['1Time Airline', 'RPA'], '1U': ['Polyot Sirena', 'Rosja'],
                 '1V': ['Galileo International', 'USA'], '1Y': ['Electronic Data Systems Corporation', 'USA'],
                 '1Z': ['Sabre Pacific', 'Australia'], '2A': ['Deutsche Bahn', 'Niemcy'],
                 '2H': ['Thalys', 'Belgia', ' Francja', ' Niemcy', ' Holandia'], '2L': ['Helvetic Airways'],
                 '2P': ['Airphil Express|Air Philippines', 'Filipiny'], '2U': ['Atlas International Airways'],
                 '2V': ['Amtrak', 'USA'], '3K': ['Jetstar Asia'], '3Q': ['China Yunnan Airlines', 'Chiny'],
                 '4A': ['Air Kiribati', 'Kiribati'], '4D': ['Air Sinai'], '4L': ['Air Astana'],
                 '4G': ['Shenzhen Airlines', 'Chiny'], '4U': ['Germanwings', 'Niemcy'],
                 '5G': ['Skyservice Airlines', 'Kanada'], '5J': ['Cebu Pacific Air', 'Filipiny'],
                 '5L': ['Aerosur', 'Boliwia'], '5P': ['SkyEurope Airlines Hungary', 'Węgry'],
                 '5X': ['United Parcel Service'], '6U': ['Air Ukraine', 'Ukraina'], '6W': ['Saratov', 'Rosja'],
                 '6H': ['Israir Airlines|Israir', 'Izrael'], '7B': ['Krasnojarsky Airlines', 'Rosja'],
                 '7F': ['First Air'], '7K': ['Kogalymavia Air Company'], '7L': ["Sun d'Or International Airlines"],
                 '8A': ['Atlas Blue'], '8B': ['Caribbean Star Airlines'], '8C': ['Air Transport International/Horizon'],
                 '8D': ['Expo Aviation/Servant Air/Astair'], '8E': ['Bering Air'], '8F': ['Prima Charter|Fischer Air'],
                 '8G': ['Angel Airlines'], '8H': ['Heli France'], '8J': ['Komiinteravia'],
                 '8L': ['Cargo Plus Aviation/Redhill Aviation'], '8M': ['Myanmar Airways International/Maxair'],
                 '8N': ['Nordkalottflyg AB'], '8O': ['West Coast Air'], '8P': ['Pacific Coastal Airlines'],
                 '8Q': ['Onur Air Tasimacilik/Baker Aviation'],
                 '8R': ['Transporte Aereo Regional do Interior Paulista/Edelweiss Air'], '8S': ['Scorpio Aviation'],
                 '8T': ['Air Tindi'], '8U': ['Afriqiyah Airways'], '8V': ['Wright Air Service'], '8W': ['BAX Global'],
                 '8Y': ['Air Burundi'], '8Z': ['Linea Aerea de Servicio Ejecutivo Regional'], '9D': ['Perm Airlines'],
                 '9E': ['Pinnacle Airlines'], '9R': ['Phuket Air'], '9U': ['Air Moldova', 'Mołdawia'],
                 '9W': ['Jet Airways'], 'AA': ['American Airlines', 'USA'], 'AB': ['Air Berlin', 'Niemcy'],
                 'AC': ['Air Canada', 'Kanada'],
                 'AD': ['Air Paradise', 'Indonezja', ' Avialeasing Company', 'Uzbekistan'],
                 'AE': ['Mandarin Airlines', 'Tajwan'], 'AF': ['Air France', 'Francja'],
                 'AG': ['Air Contractors', 'Irlandia'], 'AH': ['Air Algerie', 'Algieria'], 'AI': ['Air India', 'Indie'],
                 'AJ': ['Aero Contractors Company of Nigeria', 'Nigeria'], 'AK': ['Air Asia', 'Malezja'],
                 'AL': ['Skyway Airlines/Midwest Connect', 'USA', ' Transaviaexport Cargo Airline', 'Białoruś'],
                 'AM': ['Aeroméxico/Aerovias de Mexico', 'Meksyk'], 'AN': ['Ansett Australia', 'Australia'],
                 'AO': ['Trans Australia Airlines|Australian Airlines', 'Australia'], 'AP': ['Air One', 'Włochy'],
                 'AQ': ['Aloha Airlines', 'USA'], 'AR': ['Aerolíneas Argentinas', 'Argentyna'],
                 'AS': ['Alaska Airlines', 'USA'], 'AT': ['Royal Air Maroc', 'Maroko'],
                 'AU': ['Austral|Austral Lineas Aureas-Cielos del Sur', 'Argentyna'],
                 'AV': ['Avianca', 'Aerovias Nacionales de Colombia', 'Kolumbia'],
                 'AW': ['Schreiner Airways', 'Holandia', ' Dirgantara Air Services', 'Indonezja'],
                 'AX': ['Trans State Airlines/American Connection', 'USA', ' Binter', 'Hiszpania'],
                 'AY': ['Finnair', 'Finlandia'], 'AZ': ['Alitalia', 'Włochy'], 'A2': ['Cielos del Peru', 'Argentyna'],
                 'A3': ['Aegean Airways', 'Grecja'], 'A4': ['Southern Winds', 'Argentyna'],
                 'A5': ['Airlinair', 'Francja'],
                 'A6': ['Air Alps Aviation', 'Austria', ' KLM Alps', 'Austria'],
                 'A7': ['Air Comet', 'Hiszpania'], 'A8': ['Benin Golf Air', 'Benin'],
                 'A9': ['Airzena Georgian Airlines', 'Gruzja'], 'BA': ['British Airways', 'Wlk. Brytania'],
                 'BB': ['Seaborne Airlines', 'USA'], 'BC': ['Skymark Airlines', 'Japonia'],
                 'BD': ['British Midland Airways/bmi', 'Wlk. Brytania'],
                 'BE': ['Jersey European Airways/Flybe', 'Wlk. Brytania'],
                 'BF': ['Bluebird Cargo', 'Iceland', ' Aero-Service', 'Kolumbia'],
                 'BG': ['Biman Bangladesh Airlines', 'Bangladesz'], 'BH': ['Hawkair Aviation Services', 'Kanada'],
                 'BI': ['Royal Brunei Airlines', 'Brunei'], 'BJ': ['Nouvelair', 'Tunezja'],
                 'BK': ['Potomac Air', 'USA'], 'BL': ['Jetstar Pacific Airlines|Pacific Airlines', 'Wietnam'],
                 'BM': ['Bayu Indonesia Air', 'Indonezja', ' Air Sicilia', 'Włochy'],
                 'BN': ['Forward Air International Airlines', 'USA', ' Horizon Airlines', 'Australia'],
                 'BO': ['Bouraq Indonesia Airlines', 'Indonezja'], 'BP': ['Air Botswana', 'Botswana'],
                 'BQ': ['Aeromar Airlines', 'Dominikana'], 'BR': ['EVA Airways', 'Tajwan'],
                 'BS': ['British International Helicopters', 'Wlk. Brytania'], 'BT': ['Air Baltic', 'Łotwa'],
                 'BU': ['Braathens', 'Norwegia'], 'BV': ['Blue Panorama Airlines', 'Włochy'],
                 'BW': ['British West Indian Airways', 'Trynidad i Tobago'], 'BX': ['Coast Air', 'Norwegia'],
                 'BY': ['Britannia Airways', 'Wlk. Brytania'],
                 'BZ': ['Keystone Air Service', 'Kanada', ' Blue Dart Aviation', 'Indie'],
                 'B2': ['Belavia', 'Białoruś'], 'B3': ['Beliview Airlines', 'Nigeria'],
                 'B4': ['B.A.C.H. Flugbetriebs', 'Niemcy', ' Bankair', 'USA'], 'B5': ['Amadeus Flugdienst', 'Niemcy'],
                 'B6': ['jetBlue Airways', 'USA'], 'B7': ['UNI Airways', 'Tajwan'], 'B8': ['Eritrean Airways'],
                 'B9': ['Iran Air Tours', 'Iran', ' Air Bangladesh', 'Bangladesz'], 'CA': ['Air China'],
                 'CB': ['Suckling Airways'], 'CC': ['Air Atlanta Icelandic/Macair Airlines'], 'CD': ['Alliance Air'],
                 'CE': ['Nationwide Airlines', 'RPA'], 'CF': ['City Airline'], 'CG': ['Airlines of Paupa New Guinea'],
                 'CH': ['Bermidji Airlines'], 'CI': ['China Airlines', 'Tajwan'], 'CJ': ['China Northern Airlines'],
                 'CK': ['China Cargo Airlines'], 'CL': ['Lufthansa CityLine'], 'CM': ['Compania Panamena de Aviacion'],
                 'CN': ['Westward Airways/Islands Nationair'], 'CO': ['Continental Airlines', 'USA'],
                 'CP': ['Canadian Airlines International/Canadian Pacific Airlines '],
                 'CQ': ['Sunshine Express Airlines'], 'CR': ['OAG Worldwide', 'Wlk. Brytania'],
                 'CS': ['Continental Micronesia '], 'CU': ['Cubana'], 'CV': ['Cargolux Airlines International'],
                 'CW': ['Air Marshall Islands'], 'CX': ['Cathay Pacific Airways', 'Hongkong'], 'CY': ['Cyprus Air'],
                 'CZ': ['China Southern Airlines'], 'C2': ['Air Luxor'], 'C3': ['Contact Air'],
                 'C4': ['Zimex Aviation Limited'], 'C5': ['Champlain Enterprises'], 'C6': ['CanJet'],
                 'C7': ['Rico Linhas Aereas'], 'C8': ['Chicago Express Airlines'], 'C9': ['Cirrus Airlines'],
                 'DA': ['Air Georgia'], 'DB': ['Brit Air'], 'DC': ['Golden Air'], 'DD': ['Conti-Flug'],
                 'DE': ['Condor', 'Niemcy'], 'DG': ['Eastern Pacific'], 'DH': ['Independence Air/DHL'],
                 'DI': ['Deutsche BA', 'Niemcy'], 'DJ': ['Virgin Blue', 'Australia'], 'DK': ['Eastland Air'],
                 'DL': ['Delta Air Lines', 'USA'], 'DM': ['A.P. Møller-Mærsk|Maersk', 'Dania'],
                 'DN': ['Air Exel Belgique'], 'DO': ['Dominicana'], 'DP': ['Air 2000'], 'DQ': ['Coastal Air Transport'],
                 'DR': ['Hyères Aero Services'], 'DS': ['Air Sénégal International'], 'DT': ['TAAG Angola Airlines'],
                 'DU': ['Hemus Air'], 'DV': ['Nantucket Airlines'], 'DW': ['Helicopter Shuttle'],
                 'DX': ['Danish Air Transport'], 'DY': ['Norwegian Air Shuttle|Norwegian'], 'DZ': ['Air Metro North'],
                 'D2': ['Damania Airways'], 'D3': ['Daallo Airlines'], 'D5': ['Nepc Airlines'], 'D6': ['Inter Air'],
                 'D7': ['Dinar Lineas Aereas'], 'D8': ['Diamond Sakha Airlines'], 'D9': ['Donavia', 'Rosja'],
                 'EA': ['European Air Express'], 'EC': ['Avialeasing Aviation'], 'ED': ['Airblue'],
                 'EE': ['Aero Airlines'], 'EF': ['Far Eastern Air Transport'], 'EG': ['Japan Asia Airways '],
                 'EH': ['Air Nippon Network/Sociedad Ecuatoriana de TransporlesAereos'],
                 'EI': ['Aer Lingus', 'Irlandia'], 'EJ': ['New England Airlines'],
                 'EK': ['Emirates', 'Zjedn. Emiraty Arabskie'], 'EL': ['Air Nippon', 'Japonia'],
                 'EM': ['Empire Airlines/Aero Benin'], 'EN': ['Air Dolomiti', 'Włochy'],
                 'EO': ['Express One International/Hewa Bora Airways'], 'EP': ['Iran Asseman Airlines', 'Iran'], 'EQ': [
                         'TAME: Transportes Aéreos Militares Ecuatorianos', 'Ekwador'], 'ER': ['Astar Air Cargo'], 'ES': ['DHL International'], 'ET': ['Ethiopian Airlines', 'Etiopia'],
                 'EU': ['Ecuatoriana de Aviación'], 'EV': ['Atlantic Southeast Airlines '], 'EW': ['Eurowings'],
                 'EX': ['Aerolineas Santo Domingo'], 'EY': ['Etihad Airways/Eagle Air'],
                 'EZ': ['Evergreen International Airlines/Sun Air of Scandinavia'], 'E2': ['Edelweiss Holdings '],
                 'E3': ['Domodedovo Airlines '], 'E4': ['Aero Asia International'], 'E5': ['Samara Airlines'],
                 'E7': ['European Aviation Air/Estafeta Carga Aerea '], 'E8': ['ALPI Eagles S.p.A.', 'Włochy'],
                 'E9': ['Boston-Maine Airways', 'USA'], 'FB': ['Bulgaria Air', 'Bułgaria'],
                 'FD': ['Thai AirAsia', 'Tajlandia'], 'FG': ['Ariana Afghan Airlines', 'Afganistan'],
                 'FI': ['Icelandair', 'Islandia'], 'FJ': ['Fiji Airways|Air Pacific'], 'FL': ['AirTran Airways'],
                 'FM': ['Federal Express Corporation'], 'FQ': ['Thomas Cook Airlines', 'Belgia'],
                 'FR': ['Ryanair', 'Irlandia'], 'FV': ['Pulkovo Aviation', 'Rosja'], 'FW': ['Fairinc', 'Japonia'],
                 'FX': ['FedEx|Fedex'], 'F9': ['Frontier Airlines'], 'GA': ['Garuda Indonesia', 'Indonezja'],
                 'GB': ['ABX Air', 'USA'], 'GC': ['Gambia International Airlines', 'Gambia'], 'GF': ['Gulf Air'],
                 'GH': ['Ghana Airways', 'Ghana'], 'GM': ['Air Slovakia', 'Słowacja'], 'GN': ['Air Gabon', 'Gabon'],
                 'GQ': ['Big Sky Airlines', 'USA'], 'GT': ['GB Airways', 'Hiszpania'], 'GW': ['Kubun Airlines'],
                 'G4': ['Allegiant Air', 'USA'], 'G5': ['Enkor', 'Rosja'], 'HG': ['Niki'], 'HM': ['Air Seychelles'],
                 'HP': ['America West Airlines'], 'HV': ['Transavia Holland', 'Holandia'], 'HY': ['Uzbekistan Airways'],
                 'H5': ['Magadan Airlines'], 'H8': ['Dalavia'], 'IB': ['Iberia', 'linie lotnicze|Iberia', 'Hiszpania'],
                 'IC': ['Indian Airlines Corporation', 'Indie'], 'IG': ['Meridiana Fly|Meridiana', 'Włochy'],
                 'IR': ['Iran Air', 'Iran'], 'IW': ['AOM French Airlines', 'Francja'], 'IY': ['Yemenia', 'Jemen'],
                 'IZ': ['Arkia Israel Airlines|Arkia', 'Izrael'], 'JJ': ['TAM Linhas Aéreas'],
                 'JK': ['Spanair', 'Hiszpania'], 'JL': ['Japan Airlines', 'Japonia'], 'JM': ['Air Jamaica', 'Jamajka'],
                 'JO': ['JALways'], 'JP': ['Adria Airways'], 'JQ': ['JetStar'], 'JS': ['Air Koryo'], 'JT': ['Lion Air'],
                 'JU': ['Jat Airways'], 'J2': ['Azal Azerbaijan Airlines', 'Azerbejdżan'], 'J7': ['Centre-Avia'],
                 'K2': ['Eurolot', 'Polska'], 'KA': ['Dragonair', 'linie lotnicze|Dragonair'],
                 'KB': ['Druk Air', 'Butan'], 'KD': ['KD Avia', 'Rosja'], 'KE': ['Korean Airlines', 'Korea Płd.'],
                 'KF': ['dawne Air Botnia Blue1', 'Finlandia'], 'KL': ['KLM Royal Dutch Airlines', 'Holandia '],
                 'KM': ['Air Malta', 'Malta'], 'KO': [' Thomson Fly', 'Anglia'], 'KQ': ['Kenya Airways', 'Kenia'],
                 'KU': ['Kuwait Airways', 'Kuwejt'], 'KV': ['Kavminvodyavia', 'Rosja'], 'KW': ['Kelowna Flightcraft'],
                 'KZ': ['Nippon Cargo Airlines', 'Japonia'], 'LA': ['Lan Chile', 'Chile'],
                 'LB': ['Lloyd Aereo Boliviano', 'Boliwia'], 'LD': ['Air Hong Kong', 'Hongkong'], 'LG': ['Luxair'],
                 'LH': ['Lufthansa', 'Niemcy'], 'LJ': ['Sierra National Airlines', 'Liberia'], 'LK': ['Air Luxor'],
                 'LN': ['Libyan Airlines', 'Libia'], 'LO': ['Polskie Linie Lotnicze LOT|LOT', 'Polska'],
                 'LR': ['Lacsa/TACA Airlines|TACA'], 'LS': ['Channel Express Air Services Ltd.'],
                 'LT': ['LTU International Airways'],
                 'LX': ['Swiss International Air Lines', ' dawniej: Crossair', 'Szwajcaria'], 'LY': ['El Al', 'Izrael'],
                 'LZ': ['Balkan Bulgarian Airlines', 'Bułgaria'], 'L4': ['Lauda Air', 'Włochy'],
                 'MA': ['Malév', 'Węgry'], 'MB': ['MNG Cargo Airlines'], 'MC': ['AIR CAIRO'],
                 'MD': ['Air Madagascar', 'Madagaskar'], 'ME': ['Middle East Airlines '],
                 'MH': ['Malaysia Airlines', 'Malezja'], 'MI': ['Silkair'], 'MK': ['Air Mauritius Ltd'],
                 'MM': ['Euroatlantic Airways'], 'MP': ['Martinair', 'Holandia'],
                 'MR': ['Air Mauritania', 'Mauretania'], 'MS': ['EgyptAir', 'Egipt'],
                 'MT': ['Thomas Cook Airlines', 'Wlk. Brytania'], 'MU': ['China Eastern Airlines', 'Chiny'],
                 'MV': ['Armenian International Airways'], 'MZ': ['Merpati Nusantara Airlines'],
                 'MX': ['Mexicana de Aviación', 'Meksyk'], 'NB': ['Sterling Airlines'], 'NE': ['SkyEurope Airlines'],
                 'NG': ['Lauda Air', 'Austria'], 'NH': ['All Nippon Airways'],
                 'NI': ['Portugália Airlines', 'Portugalia'], 'NK': ['Spirit Airlines', 'USA'],
                 'NQ': ['Air Japan', 'Japonia'], 'NV': ['Air Central', 'Japonia'], 'NW': ['Northwest Airlines', 'USA'],
                 'NZ': ['Air New Zealand', 'Nowa Zelandia'], 'N3': ['Omskavia', 'Rosja'], 'OA': ['Olympic Airlines'],
                 'OB': ['Astrahan Airlines', 'Rosja'], 'OF': ['Air Finland', 'Finlandia'],
                 'OK': ['České aerolinie|Czech Airlines', 'Czechy'], 'OM': ['MIAT', 'Mongolia'], 'OO': ['SkyWest'],
                 'OS': ['Austrian Airlines', 'Austria'], 'OU': ['Croatia Airlines', 'Chorwacja'],
                 'OV': ['Estonian Air', 'Estonia'], 'OW': ['Executive Airlines', 'USA'],
                 'OX': ['Orient Thai Airlines', 'Tajlandia'], 'OZ': ['Asiana Airlines', 'Korea Płd.'],
                 'O2': ['OLT Express'], 'PE': ['Air Europe SPA'], 'PG': ['Bangkok Airways', 'Tajlandia'],
                 'PK': ['Pakistan International Airlines', 'Pakistan'], 'PR': ['Philippine Airlines', 'Filipiny'],
                 'PS': ['Ukraine International Airlines', 'Ukraina'], 'PX': ['Air Niugini'],
                 'P2': ['UTair Aviation|UTair', 'Rosja'], 'P7': ['EastLine', 'Rosja'], 'Q3': ['PB Air', 'Tajlandia'],
                 'Q5': ['40-Mile Air', 'USA'], 'QF': ['Qantas', 'Australia'],
                 'QQ': ['Alliance Airlines', ' Reno Air', 'USA'], 'QR': ['Qatar Airways', 'Katar'],
                 'QS': ['Travel Service|Travel Service Airlines'], 'QV': ['Lao Airlines '],
                 'QX': ['Horizon Air', 'USA'], 'RA': ['Royal Nepal Airlines Corporation'],
                 'RB': ['Syrian Arab Airlines'], 'RC': ['Atlantic Airways'], 'RE': ['Aer Arann'],
                 'RG': ['Varig', 'Brazylia'], 'RI': ['Mandala Airlines'], 'RJ': ['Royal Jordanian', 'Jordania'],
                 'RQ': ['Kam Air', 'Afganistan'], 'RN': ['Air Horizons'], 'RO': ['TAROM', 'Rumunia'],
                 'R2': ['Orenburg Airlines', 'Rosja'], 'R4': ['Russia Airline', 'Rosja'],
                 'SA': ['South African Airways', 'RPA'], 'SC': ['Shandong Airlines'], 'SD': ['Sudan Airways '],
                 'SG': ['Jetsgo'], 'SJ': ['Freedom Air'], 'SK': ['Scandinavian Airlines System|SAS'],
                 'SN': ['SN Brussels Airlines', 'Belgia'], 'SQ': ['Singapore Airlines', 'Singapur'],
                 'SR': ['dawniej Swissair'], 'ST': ['Germania', 'linie lotnicze|Germania', 'Niemcy'],
                 'SU': ['Aerofłot', 'Rosja'], 'SV': ['Saudia|Saudi Arabian Airlines'], 'SY': ['Sun Country Airlines'],
                 'S5': ['small planet airlines'], 'S4': ['SATA International'], 'S7': ['S7 Airlines', 'Rosja'],
                 'S9': ['East African Safari Air'], 'TE': ['FlyLAL', 'Litwa'],
                 'TG': ['Thai Airways International', 'Tajlandia'], 'TL': ['Trans Mediterranean Airways '],
                 'TK': ['Turkish Airlines', 'Turcja'], 'TN': ['Air Tahiti Nui '],
                 'TP': ['TAP Portugal|TAP Air Portugal', 'Portugalia'], 'TQ': ['Tandem Aero'], 'TR': ['Tiger Airways'],
                 'TS': ['Air Transat'], 'TT': ['Air Lithuania', 'Litwa'], 'TU': ['Tunisair', 'Tunezja'],
                 'TX': ['Air Caraibes'], 'TZ': ['ATA Airlines'], 'T4': ['Hellas Jet', 'Grecja'],
                 'T5': ['Turkmenistan', 'linie lotnicze|Turkmenistan/Akhal', 'Turkmenistan'], 'T7': ['Twin Jet'],
                 'UA': ['United Airlines', 'USA '], 'UB': ['Myanmar Airways'], 'UI': ['Eurocypria Airlines', 'Cypr'],
                 'UL': ['Air Lanka', 'Sri Lanka'], 'UM': ['Air Zimbabwe', 'Zimbabwe'],
                 'UN': ['Transaero Airlines', 'Rosja'], 'UQ': ["O'Connor Airlines", 'Australia'],
                 'US': ['US Airways', 'USA'], 'UU': ['Air Austral', 'Australia'], 'UX': ['Air Europa Lineas Aereas'],
                 'UY': ['Cameroon Airlines', 'Kamerun'], 'U2': ['easyJet', 'UK/Unix File System|UFS', 'USA'],
                 'U5': ['USA 3000 Airlines'], 'U6': ['Ural Airlines', 'Rosja'], 'U8': ['Armavia'],
                 'U9': ['Tatarstan JSC Aircompany'], 'VA': ['Volare Airlines/VIASA', 'Wenezuela'],
                 'VD': ['Air Liberte'], 'VF': ['Valuair'], 'VH': ['Aeropostal Alas de Venezuela', 'Wenezuela'],
                 'VI': ['Palmair', 'Wielka Brytania'], 'VN': ['Vietnam Airlines', 'Wietnam'],
                 'VR': ['Cape Verde Airlines', 'TACV', 'Wyspy Zielonego Przylądka'], 'VS': ['Virgin Atlantic'],
                 'VV': ['Aerosvit'], 'VY': ['Vueling Airlines', 'Hiszpania'], 'VZ': ['MyTravel Airways'],
                 'V7': ['Air Sénégal International', 'Senegal'], 'V9': ['Bashkir Airlines'], 'WF': ['Widerøe'],
                 'WH': ['China Northwest Airlines', 'China'], 'WN': ['Southwest Airlines', 'USA'],
                 'WS': ['WestJet', 'Kanada'], 'WW': ['BMI Regional', 'Wlk. Brytania'], 'WX': ['CityJet', 'Irlandia'],
                 'WY': ['Oman Air'], 'W5': ['Mahan Air'], 'W6': ['Wizz Air', 'Węgry'],
                 'X3': ['Hapag-Lloyd Express', 'Niemcy'], 'X5': ['Afrique Airlines'], 'X7': ['Chitaavia', 'Rosja'],
                 'XF': ['Vladivostok Avia'], 'XJ': ['Mesaba Airlines'], 'XK': ['CCM Airlines'],
                 'XM': ['J-Air', 'Japonia'], 'XO': ['LTE International Airways'], 'XT': ['KLM Exel'],
                 'XQ': ['SunExpress'], 'YH': ['West Caribbean Airways', 'Kolumbia'],
                 'YK': ['Air Kibris', 'Turkish Airlines'], 'YL': ['Yamal Airlines', 'Rosja'],
                 'YS': ['Régional Compagnie Aerienne Européenne'], 'YT': ['Air Togo', 'Togo'],
                 'YV': ['Mesa Airlines', 'USA'], 'YW': ['Air Nostrum'], 'YX': ['Midwest Connect'],
                 'Z2': ['Styrian Spirit', 'Austria'], 'ZA': ['Astair', 'Rosja'],
                 'ZE': ['Lineas Aereas Azteca', 'Meksyk'], 'ZI': ['Aigle Azur', 'Francja'], 'ZL': ['Regional Express'],
                 'ZN': ['Air Bourbon'], 'ZS': ['Azzura Air']}

countries = ('Afganistan', 'Albania', 'Algieria', 'Andora', 'Angola', 'Anguilla', 'Antarktyka', 'Antigua%20i%20Barbuda',
             'Arabia%20Saudyjska', 'Argentyna', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbejdżan', 'Bahamy',
             'Bahrajn', 'Bangladesz', 'Barbados', 'Belgia', 'Belize', 'Benin', 'Bermudy', 'Bhutan', 'Białoruś',
             'Boliwia', 'Bonaire Sint Eustatius i Saba', 'Bośnia%20i%20Hercegowina', 'Botswana', 'Brazylia',
             'Brunei', 'Brytyjskie Terytorium Oceanu Indyjskiego', 'Brytyjskie%20Wyspy%20Dziewicze', 'Bułgaria',
             'Burkina%20Faso', 'Burundi', 'Chile', 'Chiny', 'Chorwacja', 'Curaçao', 'Cypr', 'Czad', 'Czarnogóra',
             'Czechy', 'Dalekie%20Wyspy%20Mniejsze%20Stanów%20Zjednoczonych', 'Dania',
             'Demokratyczna%20Republika%20Konga', 'Dominika', 'Dominikana', 'Dżibuti', 'Egipt', 'Ekwador', 'Erytrea',
             'Estonia', 'Etiopia', 'Falklandy', 'Fidżi', 'Filipiny', 'Finlandia', 'Francja',
             'Francuskie Terytoria Południowe Antarktyczne', 'Gabon', 'Gambia',
             'Georgia%20Południowa%20i%20Sandwich%20Południowy', 'Ghana', 'Gibraltar', 'Grecja', 'Grenada',
             'Grenlandia', 'Gruzja', 'Guam', 'Guernsey', 'Gujana%20Francuska', 'Gujana', 'Gwadelupa', 'Gwatemala',
             'Gwinea%20Bissau', 'Gwinea%20Równikowa', 'Gwinea', 'Haiti', 'Hiszpania', 'Holandia', 'Honduras',
             'Hongkong', 'Indie', 'Indonezja', 'Irak', 'Iran', 'Irlandia', 'Islandia', 'Izrael', 'Jamajka', 'Japonia',
             'Jemen', 'Jersey', 'Jordania', 'Kajmany', 'Kambodża', 'Kamerun', 'Kanada', 'Katar', 'Kazachstan', 'Kenia',
             'Kirgistan', 'Kiribati', 'Kolumbia', 'Komory', 'Kongo', 'Korea%20Południowa', 'Korea%20Północna',
             'Kostaryka', 'Kuba', 'Kuwejt', 'Laos', 'Lesotho', 'Liban', 'Liberia', 'Libia', 'Liechtenstein', 'Litwa',
             'Luksemburg', 'Łotwa', 'Macedonia', 'Madagaskar', 'Majotta', 'Makau', 'Malawi', 'Malediwy', 'Malezja',
             'Mali', 'Malta', 'Mariany%20Północne', 'Maroko', 'Martynika', 'Mauretania', 'Mauritius', 'Meksyk',
             'Mikronezja', 'Mjanma', 'Mołdawia', 'Monako', 'Mongolia', 'Montserrat', 'Mozambik', 'Namibia', 'Nauru',
             'Nepal', 'Niemcy', 'Niger', 'Nigeria', 'Nikaragua', 'Niue', 'Norfolk', 'Norwegia', 'Nowa%20Kaledonia',
             'Nowa%20Zelandia', 'Oman', 'Pakistan', 'Palau', 'Palestyna', 'Panama', 'Papua-Nowa%20Gwinea', 'Paragwaj',
             'Peru', 'Pitcairn', 'Polinezja%20Francuska', 'Polska', 'Portoryko', 'Portugalia', 'Południowa%20Afryka',
             'Republika%20Środkowoafrykańska', 'Republika%20Zielonego%20Przylądka', 'Reunion', 'Rosja', 'Rumunia',
             'Rwanda', 'Sahara%20Zachodnia', 'Saint%20Kitts%20i%20Nevis', 'Saint%20Lucia',
             'Saint%20Vincent%20i%20Grenadyny', 'Saint-Barthélemy', 'Saint-Martin', 'Saint-Pierre%20i%20Miquelon',
             'Salwador', 'Samoa%20Amerykańskie', 'Samoa', 'San%20Marino', 'Senegal', 'Serbia', 'Seszele',
             'Sierra%20Leone', 'Singapur', 'Sint%20Maarten', 'Słowacja', 'Słowenia', 'Somalia', 'Sri%20Lanka',
             'Stany%20Zjednoczone', 'Eswatini', 'Sudan', 'Sudan%20Południowy', 'Surinam', 'Svalbard%20i%20Jan%20Mayen',
             'Syria', 'Szwajcaria', 'Szwecja', 'Tadżykistan', 'Tajlandia', 'Tajwan', 'Tanzania', 'Timor%20Wschodni',
             'Togo', 'Tokelau', 'Tonga', 'Trynidad%20i%20Tobago', 'Tunezja', 'Turcja', 'Turkmenistan',
             'Turks%20i%20Caicos', 'Tuvalu', 'Uganda', 'Ukraina', 'Urugwaj', 'Uzbekistan', 'Vanuatu',
             'Wallis%20i%20Futuna', 'Watykan', 'Wenezuela', 'Węgry', 'Wielka%20Brytania', 'Wietnam', 'Włochy',
             'Wybrzeże%20Kości%20Słoniowej', 'Wyspa%20Bouveta', 'Wyspa%20Bożego%20Narodzenia', 'Wyspa%20Man',
             'Wyspa%20Świętej%20Heleny,%20Wyspa%20Wniebowstąpienia%20i%20Tristan%20da%20Cunha', 'Wyspy%20Alandzkie',
             'Wyspy%20Cooka', 'Wyspy%20Dziewicze%20Stanów%20Zjednoczonych', 'Wyspy%20Heard%20i%20McDonalda',
             'Wyspy%20Kokosowe', 'Wyspy%20Marshalla', 'Wyspy%20Owcze', 'Wyspy%20Salomona',
             'Wyspy%20Świętego%20Tomasza%20i%20Książęca', 'Zambia', 'Zimbabwe', 'Zjednoczone%20Emiraty%20Arabskie')

country_forms = [('do', 'Afganistanu', 'Afganistan'), ('do', 'Albanii', 'Albania'), ('do', 'Algierii', 'Algieria'),
                 ('do', 'Andory', 'Andora'), ('do', 'Angoli', 'Angola'),
                 ('do', 'Anguilli', 'Anguilla'), ('do', 'Antarktyki', 'Antarktyka'),
                 ('do', 'Antigui i Barbudy', 'Antigua i Barbuda'),
                 ('do', 'Arabii Saudyjskiej', 'Arabia Saudyjska'), ('do', 'Argentyny', 'Argentyna'),
                 ('do', 'Armenii', 'Armenia'), ('do', 'Aruby', 'Aruba'), ('do', 'Australii', 'Australia'),
                 ('do', 'Austrii', 'Austria'), ('do', 'Azerbejdżanu', 'Azerbejdżan'),
                 ('na', 'Bahamów', 'Bahamy'), ('do', 'Bahrajnu', 'Bahrajn'),
                 ('do', 'Bangladeszu', 'Bangladesz'),
                 ('na', 'Barbadosu', 'Barbados'), ('do', 'Belgii', 'Belgia'),
                 ('do', 'Belize', 'Belize'), ('do', 'Beninu', 'Benin'), ('na', 'Bermudów', 'Bermudy'),
                 ('do', 'Bhutanu', 'Bhutan'),
                 ('do', 'Białorusi', 'Białoruś'), ('do', 'Boliwii', 'Boliwia'), ('do', 'Bonaire', 'Bonaire'),

                 ('do', 'Bośni i Hercegowiny', 'Bośnia i Hercegowina'), ('do', 'Botswany', 'Botswana'),
                 ('do', 'Brazylii', 'Brazylia'), ('do', 'Brunei', 'Brunei'),
                 ('na', 'Brytyjskie Wyspy Dziewicze', 'Brytyjskie Wyspy Dziewicze'), ('do', 'Bułgarii', 'Bułgaria'),
                 ('do', 'Burkiny Faso', 'Burkina Faso'), ('do', 'Burundi', 'Burundi'),
                 ('do', 'Chile', 'Chile'), ('do', 'Chin', 'Chiny'),
                 ('do', 'Chorwacji', 'Chorwacja'), ('do', 'Curaçao', 'Curaçao'), ('na', 'Cypr', 'Cypr'),
                 ('do', 'Czadu', 'Czad'), ('do', 'Czarnogóry', 'Czarnogóra'), ('do', 'Czech', 'Czechy'),
                 ('do', 'Danii', 'Dania'), ('do', 'Konga', 'Kongo'),
                 ('na', 'Dominikę', 'Dominika'), ('do', 'Dominikany', 'Dominikana'), ('do', 'Dżibuti', 'Dżibuti'),
                 ('do', 'Egiptu', 'Egipt'), ('do', 'Ekwadoru', 'Ekwador'), ('do', 'Erytrei', 'Erytrea'),
                 ('do', 'Estonii', 'Estonia'), ('do', 'Etiopii', 'Etiopia'), ('na', 'Falklandy', 'Falklandy'),
                 ('do', 'Fidżi', 'Fidżi'), ('do', 'Filipin', 'Filipiny'),
                 ('do', 'Finlandii', 'Finlandia'), ('do', 'Francji', 'Francja'),
                 ('do', 'Gabonu', 'Gabon'), ('do', 'Gambii', 'Gambia'),

                 ('do', 'Ghany', 'Ghana'),
                 ('do', 'Gibraltaru', 'Gibraltar'), ('do', 'Grecji', 'Grecja'), ('do', 'Grenady', 'Grenada'),
                 ('do', 'Grenlandii', 'Grenlandia'), ('do', 'Gruzji', 'Gruzja'), ('do', 'Guamu', 'Guam'),
                 ('do', 'Guernsey', 'Guernsey'), ('do', 'Gujany Francuskiej', 'Gujana Francuska'),
                 ('do', 'Gujany', 'Gujana'), ('do', 'Gwadelupy', 'Gwadelupa'),
                 ('do', 'Gwatemali', 'Gwatemala'),
                 ('do', 'Gwinei Bissau', 'Gwinea Bissau'),
                 ('do', 'Gwinei Równikowej', 'Gwinea Równikowa'), ('do', 'Gwinei', 'Gwinea'),
                 ('na', 'Haiti', 'Haiti'), ('do', 'Hiszpanii', 'Hiszpania'),
                 ('do', 'Holandii', 'Holandia'), ('do', 'Hondurasu', 'Honduras'), ('do', 'Hongkongu', 'Hongkong'),
                 ('do', 'Indii', 'Indie'),
                 ('do', 'Indonezji', 'Indonezja'), ('do', 'Iraku', 'Irak'), ('do', 'Iranu', 'Iran'),
                 ('do', 'Irlandii', 'Irlandia'), ('do', 'Islandii', 'Islandia'), ('do', 'Izraela', 'Izrael'),
                 ('na', 'Jamajkę', 'Jamajka'), ('do', 'Japonii', 'Japonia'), ('do', 'Jemenu', 'Jemen'),
                 ('na', 'Jersey', 'Jersey'), ('do', 'Jordanii', 'Jordania'), ('na', 'Kajmany', 'Kajmany'),
                 ('do', 'Kambodży', 'Kambodża'), ('do', 'Kamerunu', 'Kamerun'), ('do', 'Kanady', 'Kanada'),
                 ('do', 'Kataru', 'Katar'), ('do', 'Kazachstanu', 'Kazachstan'), ('do', 'Kenii', 'Kenia'),
                 ('do', 'Kirgistanu', 'Kirgistan'),
                 ('do', 'Kiribati', 'Kiribati'), ('do', 'Kolumbii', 'Kolumbia'),
                 ('na', 'Komorów', 'Komory'), ('do', 'Konga', 'Kongo'),
                 ('do', 'Korei Południowej', 'Korea Południowa'), ('do', 'Korei Północnej', 'Korea Północna'),
                 ('do', 'Kostaryki', 'Kostaryka'), ('do', 'Kuby', 'Kuba'), ('do', 'Kuwejtu', 'Kuwejt'),
                 ('do', 'Laosu', 'Laos'), ('do', 'Lesotho', 'Lesotho'), ('do', 'Libanu', 'Liban'),
                 ('do', 'Liberii', 'Liberia'), ('do', 'Libii', 'Libia'), ('do', 'Liechtensteinu', 'Liechtenstein'),
                 ('do', 'Litwy', 'Litwa'), ('do', 'Luksemburga', 'Luksemburg'), ('do', 'Łotwy', 'Łotwa'),
                 ('do', 'Macedonii', 'Macedonia'), ('do', 'Madagaskaru', 'Madagaskar'), ('do', 'Majotty', 'Majotta'),
                 ('do', 'Makau', 'Makau'), ('do', 'Malawi', 'Malawi'),
                 ('na', 'Malediwy', 'Malediwy'), ('do', 'Malezji', 'Malezja'),
                 ('do', 'Mali', 'Mali'), ('na', 'Maltę', 'Malta'), ('do', 'Marianów Północnych', 'Mariany Północne'),
                 ('do', 'Maroka', 'Maroko'), ('na', 'Martynikę', 'Martinika'),
                 ('do', 'Mauretanii', 'Mauretania'), ('do', 'Mauritiusu', 'Mauritius'),
                 ('do', 'Meksyku', 'Meksyk'), ('do', 'Mikronezji', 'Mikronezja'),
                 ('do', 'Mjanmy', 'Mjanma'), ('do', 'Mołdawii', 'Mołdawia'),
                 ('do', 'Monaka', 'Monako'), ('do', 'Mongolii', 'Mongolia'),
                 ('do', 'Montserratu', 'Montserrat'), ('do', 'Mozambiku', 'Mozambik'),
                 ('do', 'Namibii', 'Namibia'), ('do', 'Nauru', 'Nauru'), ('do', 'Nepalu', 'Nepal'),
                 ('do', 'Niemiec', 'Niemcy'), ('do', 'Nigru', 'Niger'),
                 ('do', 'Nigerii', 'Nigeria'), ('do', 'Nikaragui', 'Nikaragua'),
                 ('do', 'Niue', 'Niue'), ('do', 'Norfolku', 'Norfolk'),
                 ('do', 'Norwegii', 'Norwegia'), ('do', 'Nowej Kaledonii', 'Nowa Kaledonia'),
                 ('do', 'Nowej Zelandii', 'Nowa Zelandia'), ('do', 'Omanu', 'Oman'), ('do', 'Pakistanu', 'Pakistan'),
                 ('do', 'Palau', 'Palau'),
                 ('do', 'Palestyny', 'Palestyna'),
                 ('do', 'Panamy', 'Panama'), ('do', 'Papui-Nowej Gwinei', 'Papua-Nowa Gwinea'),
                 ('do', 'Paragwaju', 'Paragwaj'), ('do', 'Peru', 'Peru'),
                 ('do', 'Polinezji Francuskiej', 'Polinezja Francuska'),
                 ('do', 'Polski', 'Polska'), ('do', 'Portoryka', 'Portoryko'),
                 ('do', 'Portugalii', 'Portugalia'), ('do', 'Południowej Afryki', 'Południowa Afryka'),
                 ('do', 'Republiki Środkowoafrykańskiej', 'Republika Środkowoafrykańska'),
                 ('do', 'Republiki Zielonego Przylądka', 'Republika Zielonego Przylądka'), ('na', 'Reunion', 'Reunion'),
                 ('do', 'Rosji', 'Rosja'), ('do', 'Rumunii', 'Rumunia'), ('do', 'Rwandy', 'Rwanda'),
                 ('do', 'Sahary Zachodniej', 'Sahara Zachodnia'),
                 ('do', 'Saint Kitts i Nevisu', 'Saint Kitts i Nevis'),
                 ('na', 'Saint Lucia', 'Saint Lucia'),
                 ('do', 'Saint Vincent i Grenadyny', 'Saint Vincent i Grenadyny'),
                 ('na', 'Saint-Barthélemy', 'Saint-Barthélemy'), ('na', 'Saint-Martin', 'Saint-Martin'),
                 ('do', 'Saint-Pierre Miquelon', 'Saint-Pierre Miquelon'), ('do', 'Salwadoru', 'Salwador'),
                 ('do', 'Samoa Amerykańskiego', 'Samoa Amerykańskie'), ('do', 'Samoy', 'Samoa'),
                 ('do', 'San Marino', 'San Marino'), ('do', 'Senegalu', 'Senegal'), ('do', 'Serbii', 'Serbia'),
                 ('na', 'Seszele', 'Seszele'), ('do', 'Sierry Leone', 'Sierra Leone'),
                 ('do', 'Singapuru', 'Singapur'), ('na', 'Sint Maarten', 'Sint Maarten'),
                 ('do', 'Słowacji', 'Słowacja'), ('do', 'Słowenii', 'Słowenia'), ('do', 'Somalii', 'Somalia'),
                 ('na', 'Sri Lankę', 'Sri Lanka'), ('do', 'USA', 'Stany Zjednoczone'), ('do', 'Eswatini', 'Eswatini'),
                 ('do', 'Sudanu', 'Sudan'), ('do', 'Sudanu Południowego', 'Sudan Południowy'),
                 ('do', 'Surinamu', 'Surinam'),
                 ('do', 'Syrii', 'Syria'),
                 ('do', 'Szwajcarii', 'Szwajcaria'), ('do', 'Szwecji', 'Szwecja'),
                 ('do', 'Tadżykistanu', 'Tadżykistan'), ('do', 'Tajlandii', 'Tajlandia'), ('do', 'Tajwanu', 'Tajwan'),
                 ('do', 'Tanzanii', 'Tanzania'), ('do', 'Timoru Wschodniego', 'Timor Wschodni'),
                 ('do', 'Toga', 'Togo'), ('do', 'Tokelau', 'Tokelau'),
                 ('do', 'Tonga', 'Tonga'), ('do', 'Trynidadu i Tobago', 'Trynidad i Tobago'),
                 ('do', 'Tunezji', 'Tunezja'), ('do', 'Turcji', 'Turcja'), ('do', 'Turkmenistanu', 'Turkmenistan'),
                 ('do', 'Turks i Caicos', 'Turks i Caicos'), ('do', 'Tuvalu', 'Tuvalu'),
                 ('do', 'Ugandy', 'Uganda'), ('do', 'Ukrainy', 'Ukraina'),
                 ('do', 'Urugwaju', 'Urugwaj'), ('do', 'Uzbekistanu', 'Uzbekistan'),
                 ('do', 'Vanuatu', 'Vanuatu'),
                 ('do', 'Watykanu', 'Watykan'), ('do', 'Wenezueli', 'Wenezuela'), ('do', 'Węgier', 'Węgry'),
                 ('do', 'Wielkiej Brytanii', 'Wielka Brytania'), ('do', 'Wietnamu', 'Wietnam'),
                 ('do', 'Włoch', 'Włochy'), ('do', 'Wybrzeża Kości Słoniowej', 'Wybrzeże Kości Słoniowej'),
                 ('na', 'Wyspę Bożego Narodzenia', 'Wyspa Bożego Narodzenia'),
                 ('na', 'Wyspę Man', 'Wyspa Man'), (
                     'na', 'Wyspę Świętej Heleny', 'Wyspa Świętej Heleny'),
                 ('na', 'Wyspy Alandzkie', 'Wyspy Alandzkie'), ('na', 'Wyspy Cooka', 'Wyspy Cooka'),
                 ('na', 'Wyspy Dziewicze Stanów Zjednoczonych', 'Wyspy Dziewicze Stanów Zjednoczonych'),
                 ('na', 'Wyspy Kokosowe', 'Wyspy Kokosowe'),
                 ('na', 'Wyspy Marshalla', 'Wyspy Marshalla'), ('na', 'Wyspy Owcze', 'Wyspy Owcze'),
                 ('do', 'Wyspy Salomona', 'Wyspy Salomona'),
                 ('na', 'Wyspy Świętego Tomasza', 'Wyspy Świętego Tomasza i Książęca'),
                 ('do', 'Zambii', 'Zambia'),
                 ('do', 'Zimbabwe', 'Zimbabwe'),
                 ('do', 'Zjednoczonych Emiratów Arabskich', 'Zjednoczone Emiraty Arabskie')]


# """
#     [{'code': 'CFU', 'airportName': 'Ioannis Kapodistrias', 'cityName': 'Korfu', 'cityCode': 'cfu', 'countryName': 'Grecja', 'countryCode': 'gr', 'continentCode': 'eu', 'cityTo': 'do Korfu', 'cityNameToForm': 'do Korfu'}, {'code': 'WMI', 'airportName': 'Modlin', 'cityName': 'Warszawa', 'cityCode': 'waw', 'countryName': 'Polska', 'countryCode': 'pl', 'continentCode': 'eu', 'cityFrom': 'z Warszawy', 'cityNameFromForm': 'z Warszawy'}]
# """
# class Airport(models.Model):
#     airport_name = models.CharField(max_length=55)
#     airport_code = models.CharField(max_length=5)
#     city_name = models.CharField(max_length=55)
#     city_name_form = models.CharField(max_length=55)
#     country_name = models.CharField(max_length=55)
#     country_code =  models.CharField(max_length=10)
#     country_name_form = models.CharField(max_length=55)
# """


class FillDbEsky:
    def __init__(self, api_link):
        self.api_link = api_link

    def get_city_form(self):
        pass

    def get_country_form(self, country):
        self.country = country
        link = 'https://pl.wiktionary.org//w/api.php?action=parse&format=json&page=' + self.country.replace(' ','%20') + '&prop=wikitext&disablelimitreport=1&disablestylededuplication=1&disabletoc=1&utf8=1&formatversion=latest'
        page = requests.get(link)
        try:
            wikitext = page.json()['parse']['wikitext']
            country_form = wikitext[wikitext.find('Dopełniacz') + 16:wikitext.find('\n')]
            if '<ref>' in country_form:
                country_form = country_form[country_form.find("<ref>"):country_form.find("<ref>")]

            if len(country_form) < 100 and "Wysp" not in self.country:
                country_form = 'do ' + country_form
                return country_form
            elif len(country_form) < 100 and "Wyspy" in country:
                country_form = 'na ' + self.country
                return country_form
            elif len(country_form) < 100 and "Wyspa" in country:
                country_form = 'na ' + self.country_form.replace('Wyspa', 'Wyspę')
                return country_form
            else:
                country_form = 'do ' + self.country_form
                return country_form

        except KeyError:
            self.country_form = 'do ' + self.country

    def cities(self):
        esky = UnzipUrls(self.api_link)
        esky_data = esky.fetch_flight_data()
        airports = []

        for row in esky_data:
            fields_to_extract = ['arrival', 'departure']
            for my_type in fields_to_extract:
                if my_type == "arrival":
                    city_name_form = row[my_type]['cityNameToForm']
                else:
                    city_name_form = row[my_type]['cityFrom']

                for i in country_forms:
                    if i[2] == row[my_type]['countryName']:
                        country_name_form = i[0] + ' ' + i[1]

                        break

                airports.append((row[my_type]['airportName'], row[my_type]['code'], row[my_type]['cityName'],
                                 row[my_type]['cityCode'], city_name_form, row[my_type]['countryName'],
                                 row[my_type]['countryCode'], country_name_form, row[my_type]['continentCode']))

        return set(airports)

    def cities_notin_db(self):
        esky = UnzipUrls(self.api_link)
        esky_data = esky.fetch_flight_data()
        airports = []

        for row in esky_data:
            fields_to_extract = ['arrival', 'departure']
            for my_type in fields_to_extract:
                if my_type == "arrival":
                    city_name_form = row[my_type]['cityNameToForm']
                else:
                    city_name_form = row[my_type]['cityFrom']

                for i in country_forms:
                    if i[2] == row[my_type]['countryName']:
                        country_name_form = i[0] + ' ' + i[1]

                        break

                airports.append((row[my_type]['airportName'], row[my_type]['code'], row[my_type]['cityName'],
                                 row[my_type]['cityCode'], city_name_form, row[my_type]['countryName'],
                                 row[my_type]['countryCode'], country_name_form, row[my_type]['continentCode']))

        return set(airports)


"""
            airport_name = models.CharField(max_length=55)
            airport_code = models.CharField(max_length=5, primary_key=True)
            city_name = models.CharField(max_length=55)
            city_code = models.CharField(max_length=5)
            
            city_name_form = models.CharField(max_length=55)
            country_name = models.CharField(max_length=55)
            country_code =  models.CharField(max_length=10)
            country_name_form = models.CharField(max_length=55)
            continent_code = models.CharField(max_length=5)
    """


# cnx = get_connection()
#
# sql = ""
# cursor = cnx.cursor()
# try:
#     cursor.execute(sql)
#     print("rekord dodany")
# except:
#     print("Błąd!")
#
# cursor.close()
#
# cnx.close()


def airlines(self):
    pass


# connecting database in pure python, not django!

def get_connection():
    cnx = connect(
        user="postgres",
        password="coderslab",
        host="localhost",
        database="producthunt"
    )
    cnx.autocommit = True
    return cnx


class UnzipUrls:
    def __init__(self, flight_url):
        self.flight_url = flight_url

    def fetch_flight_data(self):
        if "ryanair.com" in self.flight_url:
            link = urlparse(self.flight_url)
            flight_data = parse_qs(link.query)
            return flight_data
        elif "wizzair.com" in self.flight_url:
            link = self.flight_url
            flight_data = link.split('/')
            return flight_data
        elif "esky" and "api" in self.flight_url:
            deals = requests.get(self.flight_url).json()['deals']
            return deals


if __name__ == "__main__":

    # execute only if run as a script
    url = 'https://www.ryanair.com/pl/pl/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2020-07-02&dateIn=2020-07-09&originIata=KRK&destinationIata=TRF&isConnectedFlight=false&isReturn=true&discount=0&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2020-07-02&tpEndDate=2020-07-09&tpOriginIata=KRK&tpDestinationIata=TRF&tpIsConnectedFlight=false&tpIsReturn=true&tpDiscount=0&TimeOut=13:40&TimeIn=16:10&FareKeyOut=0~N~%20~FR~NADU6~ADU6~~0~1~~X&FareKeyIn=0~T~%20~FR~TZ2LOW~BND2~~0~1~~X&flightKeyOut=FR~8508~%20~~KRK~07%2F02%2F2020%2013:40~TRF~07%2F02%2F2020%2015:45~~&flightKeyIn=FR~8507~%20~~TRF~07%2F09%2F2020%2016:10~KRK~07%2F09%2F2020%2018:10~~'
    url2 = 'https://wizzair.com/pl-pl/#/booking/select-flight/GDN/LTN/2020-05-30/2020-06-03/2/2/0/0/'
    url3 = 'https://www2.esky.pl/api/v1.0/deals.json'

    # ryaniar = UnzipUrls(url)
    # # wizz_air = UnzipUrls(url2)
    # ryanair_data = ryaniar.fetch_flight_data()
    # # wizz_data = wizz_air.fetch_flight_data()
    # # esky = UnzipUrls(url3)
    # # esky_data = esky.fetch_flight_data()
    # # # print(esky_data)
    # for i in ryanair_data:
    #     print(i, ryanair_data[i])
    # print(wizz_data[7]) # wizz air
    # table = []

    # for i in esky_data:
    #     table.append(i['arrival'])
    #     table.append(i['departure'])
    #
    # country_names = []
    # for i in table:
    #     country_names.append(i['countryName'])

    import mwclient

    # site = mwclient.Site('pl.wikipedia.org')
    # page = site.pages["ISO 3166-1 alfa-2"]
    # countries = page.text().split('-\n|')
    # countries = [country.split('\n|') for country in countries]

    # site = mwclient.Site('pl.wiktionary.org')
    # new_country_form = []
    # collect genetive forms for cauntries
    """i = 0
    new_country_form = []
    for country in countries:

        link = 'https://pl.wiktionary.org//w/api.php?action=parse&format=json&page=' + country + '&prop=wikitext&disablelimitreport=1&disablestylededuplication=1&disabletoc=1&utf8=1&formatversion=latest'
        page = requests.get(link)
        try:
            wikitext = page.json()['parse']['wikitext']
            country_form = wikitext[wikitext.find('Dopełniacz') + 16:wikitext.find('\n')]
            if len(country_form) < 100 and "Wysp" not in country:
                new_country_form.append(('do', country_form, page.json()['parse']['title']))
                print(country_form)
            elif len(country_form) < 100 and "Wysp" in country:
                new_country_form.append(('na', page.json()['parse']['title'], page.json()['parse']['title']))
                print(country_form)
            else:
                new_country_form.append(('do', page.json()['parse']['title'], page.json()['parse']['title']))
                print('długa strona', page.json()['parse']['title'])


        except KeyError:
            print('nie udało się z tym: ', country)
            new_country_form.append(('do', 'ERROR: ' + str(i), country))

        i += 1"""

    # for string in country_forms:
    #
    #     new_country_form.append(i, country))

    # connect to database
    # username = "postgres"
    # passwd = "coderslab"
    # hostname = "127.0.0.1"  # lub "localhost"
    # db_name = "producthunt"
    #
    # cnx = ConnectDb(username, passwd, hostname, db_name)
    #

    # nowa = FillDbEsky(url3).cities()
    #
    # for i in nowa:
    #     print(i)  #
    # # cnx.end()

    """
        site = mwclient.Site('pl.wikipedia.org')
        page = site.pages["Kod linii IATA"]
        lista = page.text().split('/n')
        import mwclient
        site = mwclient.Site('pl.wiktionary.org')
        page1 = site.pages("Wielka Brytania")
    
        page1 = site.pages["Wielka Brytania"]
        page2 = site.pages["Rosja"]
        lista1 = page1.text().split('\n')
        lista2 = page2.text().split('\n')
        for i in lista3:
        if "Dopełniacz" in i:
            nameForm = i[17:]
            print(nameForm)
            break
    """
    import requests

    urlm = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/PL/PLN/pl-PL/WAW-sky/LCA-sky/2020-06-01"

    querystring = {"inboundpartialdate":"2020-12-01"}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "c073021274msh87b5e91953a11e6p1e1e21jsnaf9440626a14"
        }

    response = requests.request("GET", urlm, headers=headers, params=querystring)
    print(response.text)

    headers2 = {
        'Host': 'be.wizzair.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://wizzair.com/pl-pl/',
        'Content-Type': 'application/json;charset=utf-8',
        'X-RequestVerificationToken': 'cfad26e9cc264f4a98dea95158650a3c',
        'Content-Length': '235',
        'Origin': 'https://wizzair.com',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'TE': 'Trailers',
    }