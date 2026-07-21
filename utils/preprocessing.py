import re


class TextPreprocessor:

    def __init__(self):

        # ==========================================
        # Sinonim Nama Universitas
        # ==========================================

        self.synonyms = {

            "unimal": "universitas malikussaleh",

            "kampus": "universitas malikussaleh",

            "univ malikussaleh": "universitas malikussaleh",

            "univ":"universitas malikussaleh"

        }

        # ==========================================
        # Normalisasi Kata
        # ==========================================

        self.normalization = {

            # Media Sosial
            "medsos": "media sosial",
            "sosmed": "media sosial",
            "ig": "instagram",
            "insta": "instagram",

            # Website
            "web": "website",
            "homepage": "website",
            "situs": "website",
            "url": "website",

            # Telepon
            "telp": "telepon",
            "tlp": "telepon",
            "no": "nomor",

            # Email
            "e-mail": "email",
            "mail": "email",

            # Pertanyaan
            "apakah": "apa",
            "dimanakah": "dimana",
            "siapakah": "siapa",
            "kapankah": "kapan",
            "bagaimanakah": "bagaimana",
            "buat" : "membuat",
            "daftar" :"mendaftar",

            # Bahasa sehari-hari
            "gimana": "bagaimana",
            "gmana": "bagaimana",
            "gmn": "bagaimana",
            "dmn": "dimana",

            # Nama Fakultas
            "ft": "fakultas teknik",
            "feb": "fakultas ekonomi dan bisnis",
            "fkip": "fakultas keguruan dan ilmu pendidikan",
            "fisip": "fakultas ilmu sosial dan ilmu politik",
            "fp" : "fakultas pertanian",
            "fk" : "fakultas kedokteran",
            "fh" : "fakultas hukum",

            # Singkatan Wakil Rektor
            "wr1" : 'wakil rektor 1',
            "wri" : 'wakil rektor i',
            "wr2" : 'wakil rektor 2',
            "wrii" : 'wakil rektor ii',
            "wr3" : 'wakil rektor 3',
            "wriii" : 'wakil rektor iii',

            #singkatan prodi
            "kaprodi" : "ketua prodi",
            "kepala prodi" : "ketua prodi",
            "kajur" : "ketua jurusan",
            "kepala jurusan" : "ketua jurusan",
            "sekjur" : "sekretaris jurusan",
            "akred" : "akreditasi",
            "ti" : "teknik informatika",
            "tif" : "teknik informatika",
            "it" : "teknik informatika",
            "si" : "sistem informasi",
            "sisfo" : "sistem informasi",
            "elektro" : "teknik elektro",
            "tekim" : "teknik kimia",
            "sipil" : "teknik sipil",
            "arsitektur" : "teknik arsitektur",
            "logistik" : "teknik logistik",
            "material" : "teknik material",
            "industri" : "teknik industri",
            "ekp" : "ekonomi pembangunan",
            "ekis" : "ekonomi syariah",
            "mti" : "magister teknologi informasi",
            "s2 teknologi informasi" : "magister teknologi informasi",
            "s2 informatika" : "magister teknologi informasi",
            "energi terbarukan" : "teknik energi terbarukan",
            "teknik terbarukan" : "teknik energi terbarukan",
            "s2 teknik energi terbarukan" : "teknik energi terbarukan",
            "s2 teknik terbarukan" : "teknik energi terbarukan",
            "s2 energi terbarukan" : "teknik energi terbarukan",
            "s2 teknik sipil" : "magister teknik sipil",
            "mts" : "magister teknik sipil",
            "kwu" : "kewirausahaan",
            "s2 ilmu manajemen" : "magister ilmu manajemen",
            "s2 manajemen" : "magister ilmu manajemen",
            "magister manajemen" : "magister ilmu manajemen",
            "s2 ilmu akuntansi" : "magister ilmu akuntansi",
            "s2 akuntansi" : "magister ilmu akuntansi",
            "magister akuntansi" : "magister ilmu akuntansi",
            "s2 ekonomi pembangunan" : "magister ekonomi pembangunan",
            "magister ekp" : "magister ekonomi pembangunan",
            "s2 ekp" : "magister ekonomi pembangunan",
            "ilkom" : "ilmmu komunikasi",
            "ilpol" : "ilmmu politik",
            "adm bisni" : "administrasi bisnis",
            "adm_publik" : "administrasi publik",
            "s2 sosiologi" : "magister sosiologi",
            "s2 administrasi publik" : "magister administrasi publik",
            "s2 adm publik" : "magister administrasi publik",
            "magister adm publik" : "magister administrasi publik",
            "magister ilkom" : "magister ilmu komunikasi",
            "s2 ilmu komunikasi" : "magister ilmu komunikasi",
            "s2 ilkom" : "magister ilmu komunikasi",
            "s2 ilmu hukum" : "magister ilmu hukum",
            "s3 ilmu hukum" : "s3 doktor ilmu hukum",
            "aet" : "agroekoteknologi",
            "agro" : "agroekoteknologi",
            "agb" : "agribisnis",
            "agri": "agribisnis",
            "krlautan" : "ilmu kelautan",
            "s2 agroekoteknologi":"magister agroekoteknologi",
            "s2 aet":"magister agroekoteknologi",
            "s2 agro":"magister agroekoteknologi",
            "s2 agribisnis" : "magister agribisnis",
            "s2 agb" : "magister agribisnis",
            "s2 agri" : "magister agribisnis",
            "vokasional mesin" : "vokasional teknik mesin",
            "vokasional" : "vokasional teknik mesin",
            "pertanian" : "fakultas pertanian",
            "email unimal" : "email institusi",
            "email kampus" : "email institusi",
            "email mahasiswa" : "email institusi",
            "email dosen" : "email institusi",
            "email universitas malikussaleh" : "email institusi",
            "hosting" : "web hosting",
            "email saya" : "email institusi",
            "portal" : "portal akademik",
            "portal unimal" : "portal akademik",
            "portal.unimal.ac.id" : "portal unimal",
            "portal saya" : "portal akademik",
            "e-learning" : "elearning",
            "elearning saya" : "elearning",
            "e-learning saya" : "elearning",
            "wi-fi" : "wifi",
            "wifi unimal" : "wifi",
            "wi-fi unimal" : "wifi",
            "wifi kampus" : "wifi",
            "wi-fi kampus" : "wifi",
            "kartu rencana studi" :"krs",
            "kartu studi" : "krs",
            "krs saya" : "krs",
            "kartu hasil studi" : "khs",
            "nilai semester" : "khs",
            "khs saya" : "khs",
            "transkrip nilai" : "transkrip",
            "legalisir" : "ijazah",
            "skl" : "ijazah",
            "ijazah saya" : "ijazah",
            "skl saya" : "skl",
            "surat keterangan lulus" : "ijazah",
            "surat lulus" : "ijazah",
            "surat keterangan aktif" : "surat aktif",
            "surat aktif saya" : "surat aktif",
            "cuti akademik" : "cuti kuliah",
            "cuti" : "cuti kuliah",
            "akses" : "mengakses",
            "surat pengantar magang" : "surat pengantar",
            "surat pengantar praktek" : "surat pengantar",
            "surat pengantar kp" : "surat pengantar",
            "mengurus" : "pengurusan",
            "uang kuliah" : "ukt",
            "uang kuliah tunggal" : "ukt",
            "bayar" : "membayar",
            "ukt unimal" : "ukt",
            "penangguhan" : "penundaan",
            "meminjam" : "pinjam",
            "sirkulasi" : "pinjam",
            "ebook" : "ebook",
            "buku digital" : "e-book",
            "letak" : "alamat",
            "tes toefl" : "toefl",
            "layanan tik" : "puskom",
            "upt tik" : "puskom",
            "tik" : "puskom",
            "kuliah kerja nyata" : "kkn",
            "kip kuliah" : "kip",
            "kp" : "kerja praktek"
            

        }

    def clean(self, text):

        # ==========================================
        # Case Folding
        # ==========================================

        text = text.lower()

        # ==========================================
        # Hapus Tanda Baca
        # ==========================================

        text = re.sub(
            r"[^\w\s]",
            "",
            text
        )

        # ==========================================
        # Normalisasi Kata
        # ==========================================

        for key, value in self.normalization.items():

            text = re.sub(
                rf"\b{re.escape(key)}\b",
                value,
                text
            )

        # ==========================================
        # Sinonim Universitas
        # ==========================================

        for key, value in self.synonyms.items():

            text = re.sub(
                rf"\b{re.escape(key)}\b",
                value,
                text
            )

        # ==========================================
        # Hapus Spasi Berlebih
        # ==========================================

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text