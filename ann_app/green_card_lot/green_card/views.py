from django.shortcuts import render
from random import choice as random_winner
from .models import PersonData,LotteryEvent
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
import json
from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,charset="utf-8",decode_responses=True, db=0)


def get_lang_pack(lang):
	rus_lang_pack = {
		# base
		"user": "пользователь",
		"log_out": "выйти",
		"log_in": "войти",
		"register": "зарегистрироваться",
		# register
		"form_01": "Имя - фамилия / фамилия, имя, отчество - точно так, как указано в вашем паспорте. Если у вас только одно имя, его необходимо ввести в поле фамилии / фамилии.",
		"form_02": "Пол - мужской или женский.",
		"form_03": "Дата рождения - день, месяц, год.",
		"form_04": "Город, в котором вы родились.",
		"form_05": "Страна, в которой вы родились. Используйте название страны, в которой вы родились.",
		"form_06": "Страна права на участие в программе DV - ваша страна права на участие обычно совпадает со страной вашего рождения. Ваша страна, в которой вы имеете право на участие, не связана с местом вашего проживания или вашей национальностью, если она отличается от страны вашего рождения. Если вы родились в стране, которая не соответствует критериям, просмотрите раздел часто задаваемых вопросов, чтобы узнать, есть ли другой способ получить право на участие.",
		"form_07": "Номер паспорта, страна выдачи и дата истечения срока действия вашего действующего заграничного паспорта, срок действия которого еще не истек. Это требование не распространяется на иждивенцев. Вы должны ввести данные действующего заграничного паспорта, если вы не соответствуете требованиям для освобождения от уплаты налогов. Освобождение может применяться, если вы являетесь лицом без гражданства, гражданином страны, контролируемой коммунистами, и не можете получить паспорт от правительства страны, контролируемой коммунистами, или если вы являетесь бенефициаром индивидуального отказа, утвержденного министром внутренней безопасности и секретарем. государства. Отсутствие действительной паспортной информации лишит вас права на получение DV. Для получения дополнительной информации о том, соответствуете ли вы освобождению, см. Вопрос 12 в документе «Часто задаваемые вопросы».",
		"form_08": "Почтовый адрес:",
		"form_09": "Страна в которой ты сегодня живешь.",
		"form_10": "Телефонный номер (не обязательно).",
		"form_11": "Адрес электронной почты - адрес электронной почты, к которому у вас есть прямой доступ и который будет продолжать иметь прямой доступ после того, как мы уведомим избранных в мае следующего года. Если ваша заявка выбрана и вы ответите на уведомление о своем выборе через проверку статуса заявителя, вы получите последующее электронное письмо от Государственного департамента с уведомлением о том, что подробности вашего собеседования на иммиграционную визу доступны в проверке статуса заявителя. Государственный департамент никогда не отправит вам электронное письмо о том, что вы были выбраны для участия в программе DV. См. Раздел «Часто задаваемые вопросы» для получения дополнительной информации о процессе выбора.",
		"form_12": "Наивысший уровень образования, которого вы достигли на сегодняшний день: (1) только начальная школа, (2) некоторая средняя школа, без диплома, (3) аттестат средней школы, (4) профессиональная школа, (5) некоторые университетские курсы, ( 6) университетская степень, (7) некоторые курсы повышения квалификации, (8) степень магистра, (9) некоторые курсы докторантуры или (10) докторская степень. См. Раздел «Часто задаваемые вопросы» для получения дополнительной информации об образовательных требованиях.",
		"form_13": "Количество детей - укажите имя, дату рождения, пол, город / город рождения и страну рождения для всех живущих, не состоящих в браке детей в возрасте до 21 года, независимо от того, живут ли они с вами или собираются сопровождать или следовать за вами. присоединиться к вам, если вы иммигрируете в Соединенные Штаты. Отправьте отдельные фотографии каждого из ваших детей, используя те же технические характеристики, что и ваша собственная фотография. Обязательно включите:  всех живых родных детей;  всех живых детей, законно усыновленных вами; и  все живущие приемные дети, которые не состоят в браке и не достигли возраста 21 года на дату вашей электронной записи, даже если вы больше не состоите в законном браке с родителем ребенка, и даже если ребенок в настоящее время не проживает с вами и / или не будет иммигрировать с вами. Дети, состоящие в браке, и дети, которым на момент подачи заявки уже исполнился 21 год, не имеют права на участие в программе DV. Однако Закон о защите статуса ребенка защищает детей от «старения» при определенных обстоятельствах. Если вы подадите заявку DV до того, как вашему неженатому ребенку исполнится 21 год, а ребенку исполнится 21 год до выдачи визы, возможно, что с ним или с ней могут обращаться так, как если бы он или она были моложе 21 года для целей обработки визы. Ребенку, который уже является гражданином США или LPR, на момент подачи заявки DV не потребуется и не будет выдана Diversity Visa; вы не будете наказаны за включение или исключение таких членов семьи из вашей заявки. Неспособность перечислить всех детей, которые имеют право на участие, или указание кого-либо, кто не является вашим ребенком, лишит вас права на DV, а ваш супруг (а) и дети также не будут иметь права в качестве производных заявителей Diversity Visa.",	
		#index
		"global_text": "Обзор программы: Государственный департамент ежегодно администрирует созданную законом Программу выдачи иммиграционных виз для граждан разных стран. Раздел 203 (c) Закона об иммиграции и гражданстве (INA) предусматривает класс иммигрантов, известных как «иммигранты разнообразия», из стран с исторически низкими показателями иммиграции в Соединенные Штаты. В 2022 финансовом году будет доступно до 55 000 виз для разноплановой деятельности (DV). Регистрация в программе DV бесплатна. Кандидаты, отобранные по программе (отобранные), должны соответствовать простым, но строгим требованиям, чтобы претендовать на получение визы разнообразия. Государственный департамент определяет избранных с помощью случайного компьютерного рисунка. Государственный департамент распределяет визы по разноплановой программе между шестью географическими регионами, и ни одна страна не может получить более семи процентов доступных DV в течение одного года. Для DV-2022 лица, родившиеся в следующих странах, не имеют права подавать заявку, поскольку более 50 000 уроженцев этих стран иммигрировали в Соединенные Штаты за предыдущие пять лет: Бангладеш, Бразилия, Канада, Китай (включая САР Гонконг), Колумбия, Доминиканская Республика, Сальвадор, Гватемала, Гаити, Гондурас, Индия, Ямайка, Мексика, Нигерия, Пакистан, Филиппины, Южная Корея, Соединенное Королевство (кроме Северной Ирландии) и ее зависимые территории, а также Вьетнам. Право на участие имеют лица, родившиеся в САР Макао и на Тайване.",
		#other
		"login":"ник",
		"password":"пароль",
		"home":"Главная",
		"admin":"админ",
		"winner":"победитель",
	}

	uzb_lang_pack = {
		# base
		"user": "foydalanuvchi",
		"log_out": "tashqariga chiqish",
		"log_in": "Kirish",
		"register": "ro'yxatdan o'tish",
		# register
		"form_01": "Ism - familiya, familiya, ism, otasining ismi - pasportingizda qanday ko'rinsa, xuddi shunday. Agar sizda bitta ism bo'lsa, u familiya / familiya maydoniga kiritilishi kerak.",
		"form_02": "Jins - erkak yoki ayol.",
		"form_03": "Tug'ilgan sana - kun, oy, yil.",
		"form_04": "Siz tug'ilgan shahar.",
		"form_05": "Siz tug'ilgan davlat - Siz tug'ilgan joyda hozirda ishlatiladigan mamlakat nomidan foydalaning.",
		"form_06": "DV dasturida qatnashish huquqiga ega bo'lgan mamlakat - Sizning muvofiqlik mamlakatingiz odatda tug'ilgan mamlakatingiz bilan bir xil bo'ladi. Qabul qilish huquqiga ega bo'lgan mamlakatingiz sizning tug'ilgan mamlakatingizdan farq qiladigan bo'lsa, yashash joyingiz yoki fuqaroligingiz bilan bog'liq emas. Agar siz huquqqa ega bo'lmagan mamlakatda tug'ilgan bo'lsangiz, iltimos, boshqa savollarga javob olish uchun tez-tez beriladigan savollarni ko'rib chiqing.",
		"form_07": "Pasport raqami, berilgan davlati va amal qilish muddati tugamagan xalqaro sayohat pasportingizning amal qilish muddati. Ushbu talab qaramog'ida bo'lganlarga nisbatan qo'llanilmaydi. Agar siz ozod qilish talablariga javob bermasangiz, siz xalqaro sayohat pasporti ma'lumotlarini kiritishingiz kerak. Agar siz fuqaroligingiz yo'q bo'lsa, kommunistlar nazorati ostidagi mamlakat fuqarosi bo'lsangiz va kommunistlar nazorati ostidagi mamlakat hukumatidan pasport ololmasangiz yoki ichki xavfsizlik kotibi va kotib tomonidan tasdiqlangan shaxsiy imtiyozdan foydalanuvchi bo'lsangiz, imtiyoz qo'llanilishi mumkin. davlat. Haqiqiy pasport ma'lumotlarini kiritmaslik sizni DV uchun yaroqsiz qiladi. Imtiyozga ega bo'lishingiz yoki yo'qligingiz haqida ko'proq ma'lumot olish uchun (Tez-tez beriladigan savollar) hujjatidagi 12-savolga qarang.",
		"form_08": "Pochta manzili:",
		"form_09": "Siz bugun yashaydigan mamlakat.",
		"form_10": "Telefon raqami (ixtiyoriy).",
		"form_11": "Elektron pochta manzili - Kelasi yilning may oyida tanlanganlarni xabardor qilganimizdan so'ng, siz to'g'ridan-to'g'ri kirish huquqiga ega bo'lgan va to'g'ridan-to'g'ri kirishda davom etadigan elektron pochta manzili. Agar sizning arizangiz tanlangan bo'lsa va siz o'zingizning tanlovingiz to'g'risida bildirishnomaga Abituriyent maqomini tekshirish orqali javob bersangiz, sizga Davlat departamentidan elektron pochta orqali elektron pochta aloqasi orqali immigratsion viza bo'yicha suhbatingiz tafsilotlari Entrant Status Check-da mavjudligi to'g'risida xabar beriladi. Davlat departamenti sizga DV dasturiga tanlanganingiz haqida hech qachon elektron pochta xabarini yubormaydi. Tanlov jarayoni haqida ko'proq ma'lumot olish uchun Tez-tez so'raladigan savollarga qarang.",
		"form_12": "Bugungi kunda erishgan eng yuqori darajadagi ta'limingiz: (1) Faqat boshlang'ich maktab, (2) ba'zi bir o'rta maktab, diplom yo'q, (3) o'rta maktab diplom, (4) kasb-hunar maktabi, (5) ba'zi universitet kurslari, ( 6) Universitet darajasi, (7) Ba'zi magistr darajalari, (8) Magistr darajasi, (9) Ba'zi doktorlik darajalari yoki (10) Doktorlik. Ta'lim talablari haqida qo'shimcha ma'lumot olish uchun Tez-tez so'raladigan savollarga qarang.",
		"form_13": "Bolalar soni - 21 yoshgacha bo'lgan barcha tirik, turmushga chiqmagan bolalar uchun, ular siz bilan yashayotganidan yoki hamrohlik qilish yoki ularga ergashish niyatidan qat'i nazar, tug'ilgan kuni, jinsi, tug'ilgan shahri va tug'ilgan mamlakati ro'yxati. Qo'shma Shtatlarga ko'chib o'tishingiz kerak bo'lsa, sizga qo'shilish uchun. O'zingizning fotosuratingiz bilan bir xil texnik shartlardan foydalangan holda har bir farzandingizning individual fotosuratlarini yuboring. Bunga quyidagilarni kiriting:  barcha tirik tabiiy bolalar;  siz qonuniy ravishda asrab olingan barcha tirik bolalar; va, elektron pochta orqali kirgan kuningizda, turmush qurmagan va 21 yoshga to'lmagan barcha tirik o'gay farzandlar, agar siz endi bolaning ota-onasi bilan qonuniy nikohda bo'lmasangiz ham, va bola hozirda siz bilan yashamasa ham va / yoki siz bilan immigratsiya bo'lmaydi. Arizangizni topshirganingizda, turmush qurgan bolalar va 21 yoshga to'lgan bolalar DV dasturidan foydalana olmaydilar. Biroq, 'Bolalar maqomini himoya qilish to'g'risida' gi qonun muayyan sharoitlarda bolalarni 'qarish' dan himoya qiladi. Agar siz DV-dagi arizangizni turmushga chiqmagan farzandingiz 21 yoshga to'lgunga qadar, va bola viza berilishidan oldin 21 yoshga to'lgan taqdirda topshirsangiz, u bilan vizani qayta ishlash maqsadida 21 yoshga to'lganday munosabatda bo'lish mumkin. DV arizangizni topshirganingizda allaqachon AQSh fuqarosi yoki LPR bo'lgan bolaga turli xillik vizasi talab qilinmaydi yoki berilmaydi; bunday oila a'zolarini kiritganingiz yoki kiritmaganligingiz uchun jazolanmaysiz. Muvofiq bo'lgan barcha bolalar ro'yxatini kiritmaslik yoki sizning farzandingiz bo'lmagan birovni ro'yxatga olish DVga ega bo'lishingizga olib keladi va sizning turmush o'rtog'ingiz va farzandlaringiz, shuningdek, 'Turli xillik vizasi' uchun ariza beruvchilar sifatida qatnashmaydi.",
		#index
		"global_text": "Dasturga umumiy nuqtai: Davlat departamenti har yili qonun bilan yaratilgan 'Turli xillik uchun immigratsion viza' dasturini boshqaradi. Immigratsiya va fuqarolik to'g'risidagi qonunning (INA) 203 (s) qismida AQShga immigratsiya tarixiy jihatdan past bo'lgan mamlakatlardan 'xilma-xillik immigrantlari' deb nomlanuvchi immigrantlar toifasi nazarda tutilgan. 2022-moliya yili uchun 55000 ta turli xil vizalar (DV) mavjud bo'ladi. DV dasturiga ro'yxatdan o'tish uchun hech qanday xarajat yo'q. Dasturda tanlangan talabgorlar (tanlanganlar) xilma-xillik vizasini olish uchun oddiy, ammo qat'iy talablarga javob berishi kerak. Davlat departamenti tanlov ishtirokchilarini tasodifiy kompyuter chizmasi orqali aniqlaydi. Davlat departamenti xilma-xillik vizalarini oltita geografik mintaqalar o'rtasida taqsimlaydi va biron bir mamlakat bir yilda mavjud DV-larning etti foizidan ko'pini olishi mumkin emas. DV-2022 uchun quyidagi mamlakatlarda tug'ilgan shaxslar ariza berish huquqiga ega emaslar, chunki ushbu mamlakatlarning 50000 dan ortiq mahalliy aholisi Qo'shma Shtatlarga o'tgan besh yil ichida ko'chib kelgan: Bangladesh, Braziliya, Kanada, Xitoy (shu jumladan Gonkong SAR), Kolumbiya, Dominikan Respublikasi, Salvador, Gvatemala, Gaiti, Gonduras, Hindiston, Yamayka, Meksika, Nigeriya, Pokiston, Filippinlar, Janubiy Koreya, Buyuk Britaniya (Shimoliy Irlandiyadan tashqari) va uning qaram hududlari va Vetnam. Makao SAR va Tayvanda tug'ilgan shaxslar huquqiga ega.",
		#other
		"login":"taxallus",
		"password":"parol",
		"home":"uy",
		"admin":"admin",
		"winner":"g'olib",
	}

	tadz_lang_pack = {
		# base
		"user": "корбар",
		"log_out": "баромадан",
		"log_in": "даромадан",
		"register": "ба қайд гирифтан",
		# register
		"form_01": "Ном - насаб / насаб, ном, номи падар - ҳамон тавре ки дар шиносномаи шумо дида мешавад. Агар шумо танҳо як ном дошта бошед, он бояд ба майдони насаб / насаб дохил карда шавад.",
		"form_02": "Ҷинс - мард ё зан.",
		"form_03": "Санаи таваллуд - рӯз, моҳ, сол.",
		"form_04": "Шаҳре, ки шумо дар он таваллуд шудаед.",
		"form_05": "Кишваре, ки шумо дар он таваллуд шудаед - Номи кишвареро, ки дар айни замон барои ҷои таваллуд истифода шудааст, истифода баред.",
		"form_06": "Кишвари мувофиқ ба барномаи DV - Кишвари шумо мувофиқат одатан бо кишвари таваллудатон хоҳад буд. Кишвари мувофиқатон ба ҷои зистатон ё шаҳрвандии шумо вобаста нест, агар он аз кишвари таваллудатон фарқ кунад. Агар шумо дар кишваре таваллуд шудаед, ки қобили қабул нест, лутфан саволҳои зуд-зуд додашударо дида бароед, ки оё роҳи дигари интихоби шумо низ ҳаст.",
		"form_07": "Рақами шиноснома, кишвари додани он ва мӯҳлати ба анҷом расидани шиносномаи байналмилалии мӯҳлати эътибори ғайримуҳлати шумо. Ин талабот нисбати шахсони вобаста ба онҳо дахл надорад. Шумо бояд маълумоти дурусти шиносномаи байналмилалии сафарро ворид кунед, агар шумо ба талабот барои озодкунӣ ҷавобгӯ набошед. Озодкунӣ метавонад дар сурате татбиқ карда шавад, ки шумо шаҳрвандӣ надошта бошед, шаҳрванди як кишвари таҳти назорати коммунистӣ буда ва наметавонед аз ҳукумати ин кишвар таҳти назорати коммунистӣ шиноснома гиред ё баҳрабардорандаи радди инфиродӣ, ки онро Котиби Амнияти Миллӣ ва Котиб тасдиқ кардаанд давлат. Надоштани маълумоти дурусти шиноснома шуморо барои гирифтани DV қабул намекунад. Барои гирифтани маълумоти иловагӣ дар бораи он, ки шумо бо имтиёз ҷавобгӯ ҳастед ё не, ба саволи 12 дар ҳуҷҷати Саволҳои Такроршаванда нигаред.",
		"form_08": "Суроғаи почта:",
		"form_09": "Кишваре, ки шумо имрӯз зиндагӣ мекунед.",
		"form_10": "Рақами телефон (ихтиёрӣ).",
		"form_11": "Суроғаи почтаи электронӣ - Суроғаи почтаи электроние, ки шумо дастрасии мустақим доред ва дастрасии мустақимро идома медиҳад, пас аз огоҳ кардани интихобкунандагон дар моҳи майи соли оянда. Агар вуруди шумо интихоб шуда бошад ва шумо тавассути огоҳинома оид ба интихоби худ тавассути Санҷиши Статуси довталабон посух диҳед, шумо иртиботи паёми электронии Департаменти Давлатиро мегиред, ки шуморо огоҳ мекунад, ки тафсилоти мусоҳибаи раводиди муҳоҷирататон дар Санҷиши Статуси Санҷиш дастрас аст. Департаменти давлатӣ ҳеҷ гоҳ ба шумо паёми электронӣ намефиристад, ки дар он шумо барои барномаи DV интихоб шудаед. Барои маълумоти бештар дар бораи раванди интихоб, ба саволҳои зуд-зуд додашаванда нигаред.",
		"form_12": "Сатҳи баландтарини таҳсиле, ки шумо имрӯз ба даст овардаед: (1) Танҳо мактаби ибтидоӣ, (2) Баъзе мактаби миёна, диплом нест, (3) Дипломи мактаби миёна, (4) Мактаби касбӣ, (5) Баъзе курсҳои донишгоҳӣ, () 6) дараҷаи донишгоҳӣ, (7) Баъзе курсҳои баъдидипломӣ, (8) дараҷаи магистр, (9) баъзе курсҳои докторантура ё (10) докторантура. Барои гирифтани маълумоти иловагӣ дар бораи талаботҳои таълимӣ, ба саволҳои зуд-зуд додашаванда нигаред.",
		"form_13": "Шумораи кӯдакон - Ном, санаи таваллуд, ҷинс, шаҳр / шаҳраки таваллуд ва кишвари таваллудро барои ҳамаи кӯдакони то 21-солаи зинда, бешавҳар, новобаста аз он ки онҳо бо шумо зиндагӣ мекунанд ё нияти ҳамроҳӣ кардан ё пайравӣ карданро доранд, номбар кунед барои пайвастан ба шумо, агар шумо ба Иёлоти Муттаҳида муҳоҷират кунед. Аксҳои инфиродии ҳар як фарзанди худро бо истифода аз мушаххасоти техникии ҳамон акси шахсии худ пешниҳод кунед. Боварӣ ҳосил намоед:  ҳама кӯдакони табиии зинда;  ҳамаи кӯдакони зинда, ки аз ҷониби шумо ба таври қонунӣ ба фарзандӣ қабул карда шудаанд; ва,  ҳамаи фарзандони зиндамон, ки бешавҳар ва то 21-сола дар рӯзи вуруди электронии шумо ҳастанд, ҳатто агар шумо дигар бо падару модари кӯдак ба таври қонунӣ издивоҷ накарда бошед ва ҳатто агар кӯдак айни замон бо шумо зиндагӣ накунад ва / ё бо шумо муҳоҷират намекунад. Кӯдакони оиладор ва кӯдаконе, ки синнашон аз 21 болотар аст ва ҳангоми пешниҳоди вуруд ба барномаи DV ҳақ надоранд. Аммо, Қонун дар бораи ҳифзи мақоми кӯдак дар ҳолатҳои муайян кӯдаконро аз «пиршавӣ» муҳофизат мекунад. Агар шумо сабти DV-и худро пеш аз ба синни 21-солагӣ расидани фарзанди бешавҳар ва кӯдак 21-сола шуданаш пеш аз додани раводид пешниҳод кунед, эҳтимол дорад, ки ӯ бо ӯ тавре муносибат кунад, ки синнаш аз 21 нарасидааст. Кӯдаке, ки аллакай шаҳрванди ИМА ё LPR аст, вақте ки шумо вуруди DV-и худро пешниҳод мекунед, виза барои диверсификатсия талаб карда намешавад ё дода намешавад; барои дохил кардан ё надодани чунин аъзои оила ҷазо дода намешавад. Нокомӣ дар рӯйхати ҳамаи кӯдаконе, ки ҳуқуқ доранд ё номбар кардани касе, ки фарзанди шумо нест, шуморо барои гирифтани DV ғайри қобили қабул мегардонад ва ҳамсар ва фарзандонатон ҳамчун довталаби ҳосилаи раводиди гуногунрангӣ номувофиқ хоҳанд буд.",
		#index
		"global_text": "Шарҳи барнома: Департаменти давлатӣ ҳамасола Барномаи раводиди муҳоҷирати гуногунҷанбаеро, ки аз ҷониби қонун тартиб дода шудааст, идора мекунад. Қисми 203 (в) Қонуни муҳоҷират ва шаҳрвандӣ (INA) як синфи муҳоҷиронро бо номи «муҳоҷирони гуногунранг» аз кишварҳое, ки сатҳи таърихан паси муҳоҷират ба Иёлоти Муттаҳида доранд, пешбинӣ мекунад. Барои соли молиявии 2022, то 55,000 раводид барои гуногунрангӣ (DV) мавҷуд аст. Барои сабти ном барои барномаи DV хароҷот вуҷуд надорад. Довталабоне, ки дар барнома интихоб шудаанд (интихобкунандагон) бояд ба талаботи оддӣ, вале мутобиқати қатъӣ барои гирифтани раводиди гуногунрангӣ ҷавобгӯ бошанд. Департаменти давлатӣ интихобкунандагонро тавассути расмҳои тасодуфии компютерӣ муайян мекунад. Департаменти давлатӣ раводидҳои гуногунро байни шаш минтақаи ҷуғрофӣ тақсим мекунад ва ҳеҷ як кишвар наметавонад дар тӯли як сол беш аз ҳафт фоизи DV-ҳои мавҷударо дастрас кунад. Барои DV-2022 ашхосе, ки дар кишварҳои зерин таваллуд шудаанд, ҳаққи муроҷиатро надоранд, зеро беш аз 50,000 зодагони ин кишварҳо дар панҷ соли гузашта ба Иёлоти Муттаҳида муҳоҷират кардаанд: Бангладеш, Бразилия, Канада, Чин (аз ҷумла Гонконг САР), Колумбия, Ҷумҳурии Доминикан, Сальвадор, Гватемала, Гаити, Гондурас, Ҳиндустон, Ямайка, Мексика, Нигерия, Покистон, Филиппин, Кореяи Ҷанубӣ, Подшоҳии Муттаҳида (ба истиснои Ирландияи Шимолӣ) ва қаламравҳои тобеи он ва Ветнам. Шахсоне, ки дар Макао SAR ва Тайван таваллуд шудаанд, ҳуқуқ доранд.",
		#other
		"login":"лақаб",
		"password":"парол",
		"home":"хона",
		"admin":"администратор",
		"winner":"ғолиб",
	}	
	if lang == 'tadz':
		return tadz_lang_pack
	elif lang == 'uzb':
		return uzb_lang_pack
	else:
		return rus_lang_pack

def get_logined_UserData():
	ID = redis_instance.get('id')
	if ID: 
		return PersonData.objects.get(id = int(ID))
	else:
		return False

def index(request):
	return HttpResponseRedirect(reverse('green_card:lottery'))

def lottery(request):
	redis_instance.set('url', 'green_card:lottery')
	return render(request, 'html/lottery.html', {'lang_pack': get_lang_pack(redis_instance.get('lang')),'login': get_logined_UserData()})


def register(request):
	redis_instance.set('url', 'green_card:register')
	return render(request, 'html/register.html', {'lang_pack': get_lang_pack(redis_instance.get('lang')),'login': get_logined_UserData()})

def create(request):
	user = PersonData(
		login    = request.POST['login'   ],
		password = request.POST['password'],
		form_01  = request.POST['form_01' ],
		form_02  = request.POST['form_02' ],
		form_03  = request.POST['form_03' ],
		form_04  = request.POST['form_04' ],
		form_05  = request.POST['form_05' ],
		form_06  = request.POST['form_06' ],
		form_07  = request.POST['form_07' ],
		form_08  = request.POST['form_08' ],
		form_09  = request.POST['form_09' ],
		form_10  = request.POST['form_10' ],
		form_11  = request.POST['form_11' ],
		form_12  = request.POST['form_12' ],
		form_13  = request.POST['form_13' ],
	)

	user.save()
	redis_instance.set('id', user.id)
	
	return HttpResponseRedirect(reverse('green_card:lottery'))

def log_in(request):
	redis_instance.set('url', 'green_card:log_in')
	return render(request, 'html/login.html', {'lang_pack': get_lang_pack(redis_instance.get('lang')),'login': get_logined_UserData()})

def check(request):
	try:
		user = PersonData.objects.get(login=request.POST['login'])
		if user.password == request.POST['password']:
			redis_instance.set('id', user.id)
			return HttpResponseRedirect(reverse('green_card:lottery'))
		else:
			return HttpResponseRedirect(reverse(redis_instance.get('url')))
	except:
		return HttpResponseRedirect(reverse(redis_instance.get('url')))

def log_out(request):
	redis_instance.delete('id')
	return HttpResponseRedirect(reverse(redis_instance.get('url')))

def set_rus(request):
	redis_instance.set('lang', 'rus')
	return HttpResponseRedirect(reverse(redis_instance.get('url')))

def set_uzb(request):
	redis_instance.set('lang', 'uzb')
	return HttpResponseRedirect(reverse(redis_instance.get('url')))

def set_tadz(request):
	redis_instance.set('lang', 'tadz')
	return HttpResponseRedirect(reverse(redis_instance.get('url')))

def get_winner(request):
	redis_instance.set('url', 'green_card:get_winner')
	winner = random_winner(PersonData.objects.all())
	
	event = LotteryEvent(
		date = now(),
		winner_id = winner.id
	)

	event.save()

	return render(request, 'html/winner.html', {'lang_pack': get_lang_pack(redis_instance.get('lang')),'winner': winner.login})