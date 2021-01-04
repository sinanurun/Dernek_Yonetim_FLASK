from orm_db import *
kullanici = {}
dernek_bilgileri = {}


#giriş karşlılama sayfası
@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
    try:
        if request.method == 'POST':
            tc = request.form.get('tcno')
            sifre = request.form.get('sifre')
            uye = Uye.query.filter_by(uye_tc=tc, uye_sifre=sifre).first()
            print(uye)
            if uye.uye_durum == 0 and (uye.uye_yonetim == 0 or uye.uye_yonetim == 1):
                session['yonetici'] = uye.uye_id
                kullanici['yonetici'] = uye

                return redirect(url_for('yonetici_sayfasi'))
            elif uye.uye_durum == 0 and (uye.uye_yonetim == 2):
                session['uye'] = uye.uye_id
                kullanici['uye'] = uye
                print(1)
                return redirect(url_for('uye_sayfasi'))
            elif uye.uye_durum == 1:
                return render_template('index.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")
        else:
            return render_template('index.html', mesaj="Hoş Geldiniz")
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#çıkış işlemleri sayfası
@app.route('/cikis')
def cikis():
    session.clear()
    kullanici.clear()
    dernek_bilgileri.clear()
    return redirect(url_for('index'))


#yönetici sayfası işlemleri
@app.route('/yonetici_sayfasi', methods=['GET', 'POST'])
@app.route('/yonetici_sayfasi')
def yonetici_sayfasi():
    try:
        dernek_bilgileri = dernek_bilgisi()
        return render_template("yonetici.html",yonetici=kullanici['yonetici'],dernek_bilgileri=dernek_bilgileri)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#üye  sayfası işlemleri
@app.route('/uye_sayfasi', methods=['GET', 'POST'])
@app.route('/uye_sayfasi')
def uye_sayfasi():
    try:
        dernek_bilgileri = dernek_bilgisi()
        return render_template("uye.html", uye=kullanici['uye'], dernek_bilgileri=dernek_bilgileri)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#aidat listeleme işlemleri
@app.route('/aidat_listesi')
def aidat_listesi():
    try:
        aidatlar = Aidat.query.all()
        return render_template("aidat_listesi.html", uye=kullanici['uye'], aidatlar=aidatlar)
    except:
        return render_template("aidat_listesi.html", uye=kullanici['uye'])


# aidat listeleme işlemleri
@app.route('/uye_aidat_sayfasi')
def uye_aidat_listesi():
    try:
        uye_id = session['uye']
        aidatlar = Aidat.query.filter_by(aidat_uye_id=uye_id).all()
        return render_template("aidat_listesi.html", uye=kullanici['uye'], aidatlar=aidatlar)
    except:
        return render_template("aidat_listesi.html", uye=kullanici['uye'])


#bagis listeleme işlemleri
@app.route('/bagis_listesi')
def bagis_listesi():
    try:
        bagislar = Bagis.query.all()
        return render_template("bagis_listesi.html", uye=kullanici['uye'], bagislar=bagislar)
    except:
        return render_template("bagis_listesi.html", uye=kullanici['uye'])


#gider listeleme işlemleri
@app.route('/giderler_listesi')
def gider_listesi():
    try:
        giderler = Gider.query.all()
        return render_template("giderler_listesi.html", uye=kullanici['uye'], giderler=giderler)
    except:
        return render_template("giderler_listesi.html", uye=kullanici['uye'])


#üye ekleme işlemleri
@app.route('/uye_ekle', methods=['GET', 'POST'])
@app.route('/uye_ekle')
def uye_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                yeni_uye = Uye(uye_adi_soyadi=bilgiler['uye_adi_soyadi'], uye_tc=bilgiler['uye_tc'], uye_sifre=bilgiler['uye_adi_soyadi'],
                               uye_tel=bilgiler['uye_tel'],uye_adres=bilgiler['uye_adres'], uye_email=bilgiler['uye_email'],
                               uye_durum=int(bilgiler['uye_durum']), uye_yonetim=int(bilgiler['uye_yonetim']))
                dbsession.add(yeni_uye)
                dbsession.commit()
                return render_template("uye_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                print()
                return render_template("uye_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:
            return render_template("uye_ekle.html", yonetici=kullanici['yonetici'])
    except:
        return render_template("uye_ekle.html", yonetici=kullanici['yonetici'])


#üye listeleme işlemleri
@app.route('/uye_listesi', methods=['GET', 'POST'])
@app.route('/uye_listesi')
def uye_listesi():
    try:
        uyeler = Uye.query.all()
        return render_template("uye_listesi.html", yonetici=kullanici['yonetici'], uyeler=uyeler)
    except:
        return render_template("uye_listesi.html", yonetici=kullanici['yonetici'])


#aidat ekleme işlemleri
@app.route('/aidat_ekle', methods=['GET', 'POST'])
@app.route('/aidat_ekle')
def aidat_ekle():
    tarih = datetime.today().utcnow()
    tarih = tarih.strftime("%d/%m/%Y")
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['aidat_tarihi'], '%d/%m/%Y')
                tarih = datetime.date(tarih)
                yeni_aidat = Aidat(aidat_yonetici_id=session['yonetici'], aidat_uye_id=bilgiler['aidat_uye_id'],
                                   aidat_tutari=float(bilgiler['aidat_tutari']),
                                   aidat_tarihi=tarih,
                                   aidat_aciklama=bilgiler['aidat_aciklama'])
                dbsession.add(yeni_aidat)
                dbsession.commit()
                return render_template("aidat_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("aidat_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:
            uye_listesi = Uye.query.filter_by(uye_durum=0).all()
            return render_template("aidat_ekle.html", yonetici=kullanici['yonetici'], uye_listesi=uye_listesi, tarih=tarih)
    except:
        uye_listesi = Uye.query.filter_by(uye_durum = 0).all()
        return render_template("aidat_ekle.html", yonetici=kullanici['yonetici'],uye_listesi=uye_listesi, tarih=tarih)


#bağış ekleme işlemleri
@app.route('/bagis_ekle', methods=['GET', 'POST'])
@app.route('/bagis_ekle')
def bagis_ekle():
    tarih = datetime.today().utcnow()
    tarih = tarih.strftime("%d/%m/%Y")
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['bagis_tarihi'], '%d/%m/%Y')
                tarih = datetime.date(tarih)
                yeni_bagis = Bagis(bagis_yonetici_id=session['yonetici'], bagis_yapan=bilgiler['bagis_yapan'],
                                   bagis_tutari=float(bilgiler['bagis_tutari']), bagis_tarihi=tarih,
                                   bagis_aciklama=bilgiler['bagis_aciklama'])
                dbsession.add(yeni_bagis)
                dbsession.commit()
                return render_template("bagis_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("bagis_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarısızlık")
        else:
            return render_template("bagis_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)
    except:
        return render_template("bagis_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)


#gider ekleme işlemleri
@app.route('/gider_ekle', methods=['GET', 'POST'])
@app.route('/gider_ekle')
def gider_ekle():
    tarih = datetime.today().utcnow()
    tarih = tarih.strftime("%d/%m/%Y")
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['gider_tarihi'], '%d/%m/%Y')
                tarih = datetime.date(tarih)
                yeni_gider = Gider(gider_yonetici_id=session['yonetici'],  gider_tutari=float(bilgiler['gider_tutari']),
                                   gider_tarihi=tarih, gider_aciklama=bilgiler['gider_aciklama'])
                dbsession.add(yeni_gider)
                dbsession.commit()
                return render_template("gider_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("gider_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarısızlık")
        else:
            return render_template("gider_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)
    except:
        return render_template("gider_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)


# aidat güncelleme ve silme işlemleri
@app.route('/aidat_guncelle_sil/<int:id>')
@app.route('/aidat_guncelle_sil')
def aidat_guncelle_sil(id=0):
    if id == 0:
        aidatlar = Aidat.query.all()
        return render_template("aidat_guncelle_sil.html", yonetici=kullanici['yonetici'], aidatlar=aidatlar)
    else:
        aidatlar = Aidat.query.filter_by(aidat_id=id).first()
        return redirect(url_for('aidat_guncelle_sil'))


@app.route('/aidat_guncelle/<int:id>')
@app.route('/aidat_guncelle', methods=['GET', 'POST'])
def aidat_guncelle(id=0):
    if id != 0:
        aidatlar = Aidat.query.filter_by(aidat_id=id).first()
        return render_template("aidat_guncelle.html", yonetici=kullanici['yonetici'], aidatlar=aidatlar)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['aidat_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        dbsession.query(Aidat).filter(Aidat.aidat_id == bilgiler['aidat_id']).update({Aidat.aidat_tutari: float(bilgiler['aidat_tutari']),
                                                                                      Aidat.aidat_tarihi: tarih, Aidat.aidat_aciklama: bilgiler['aidat_aciklama']})
        dbsession.commit()
        return redirect(url_for('aidat_guncelle_sil'))
    else:
        aidatlar = Aidat.query.filter_by(aidat_id=id).first()
        print(aidatlar)
        return redirect(url_for('aidat_guncelle'))


@app.route('/aidat_sil/<int:sil>')
def aidat_sil(sil=0):
    if sil != 0:
        dbsession.query(Aidat).filter(Aidat.aidat_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('aidat_guncelle_sil'))


# bağış güncelleme ve silme işlemleri
@app.route('/bagis_guncelle_sil/<int:id>')
@app.route('/bagis_guncelle_sil')
def bagis_guncelle_sil(id=0):
    if id == 0:
        bagislar = Bagis.query.all()
        return render_template("bagis_guncelle_sil.html", yonetici=kullanici['yonetici'], bagislar=bagislar)
    else:
        bagislar = Bagis.query.filter_by(bagis_id=id).first()
        return redirect(url_for('bagis_guncelle_sil'))


@app.route('/bagis_guncelle/<int:id>')
@app.route('/bagis_guncelle', methods=['GET', 'POST'])
def bagis_guncelle(id=0):
    if id != 0:
        bagislar = Bagis.query.filter_by(bagis_id=id).first()
        return render_template("bagis_guncelle.html", yonetici=kullanici['yonetici'], bagislar=bagislar)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['bagis_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        dbsession.query(Bagis).filter(Bagis.bagis_id==bilgiler['bagis_id']).update({Bagis.bagis_yapan: bilgiler['bagis_yapan'],
                                                                                    Bagis.bagis_tutari: float(bilgiler['bagis_tutari']),
                                                                                    Bagis.bagis_tarihi: tarih, Bagis.bagis_aciklama: bilgiler['bagis_aciklama']})
        dbsession.commit()
        return redirect(url_for('bagis_guncelle_sil'))
    else:
        bagislar = Bagis.query.filter_by(bagis_id=id).first()
        return redirect(url_for('bagis_guncelle'))


@app.route('/bagis_sil/<int:sil>')
def bagis_sil(sil=0):
    if sil != 0:
        dbsession.query(Bagis).filter(Bagis.bagis_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('bagis_guncelle_sil'))


# gider güncelleme ve silme işlemleri
@app.route('/gider_guncelle_sil/<int:id>')
@app.route('/gider_guncelle_sil')
def gider_guncelle_sil(id=0):
    if id == 0:
        giderler = Gider.query.all()
        return render_template("gider_guncelle_sil.html", yonetici=kullanici['yonetici'], giderler=giderler)
    else:
        giderler = Gider.query.filter_by(gider_id=id).first()
        return redirect(url_for('gider_guncelle_sil'))


@app.route('/gider_guncelle/<int:id>')
@app.route('/gider_guncelle', methods=['GET', 'POST'])
def gider_guncelle(id=0):
    if id != 0:
        giderler = Gider.query.filter_by(gider_id=id).first()
        return render_template("gider_guncelle.html", yonetici=kullanici['yonetici'], giderler=giderler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['gider_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        dbsession.query(Gider).filter(Gider.gider_id == bilgiler['gider_id']).update({Gider.gider_tutari: float(bilgiler['gider_tutari']),
                                                                                    Gider.gider_tarihi: tarih, Gider.gider_aciklama: bilgiler['gider_aciklama']})
        dbsession.commit()
        return redirect(url_for('gider_guncelle_sil'))
    else:
        giderler = Gider.query.filter_by(gider_id=id).first()
        return redirect(url_for('gider_guncelle'))


@app.route('/gider_sil/<int:sil>')
def gider_sil(sil=0):
    if sil != 0:
        dbsession.query(Gider).filter(Gider.gider_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('gider_guncelle_sil'))


 # Üye güncelleme ve silme işlemleri
@app.route('/uye_guncelle_sil/<int:id>')
@app.route('/uye_guncelle_sil')
def uye_guncelle_sil(id=0):
    if id == 0:
        uyeler = Uye.query.all()
        return render_template("Uye_guncelle_sil.html", yonetici=kullanici['yonetici'], uyeler=uyeler)
    else:
        uyeler = Uye.query.filter_by(uye_id=id).first()
        return redirect(url_for('uye_guncelle_sil'))


@app.route('/uye_guncelle/<int:id>')
@app.route('/uye_guncelle', methods=['GET', 'POST'])
def uye_guncelle(id=0):
    if id != 0:
        uyeler = Uye.query.filter_by(uye_id=id).first()
        return render_template("uye_guncelle.html", yonetici=kullanici['yonetici'], uyeler=uyeler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        dbsession.query(Uye).filter(Uye.uye_id==bilgiler['uye_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('uye_guncelle_sil'))
    else:
        uyeler = Uye.query.filter_by(uye_id=id).first()
        return redirect(url_for('uye_guncelle'))

@app.route('/uye_sil/<int:sil>')
def uye_sil(sil=0):
    if sil != 0:
        dbsession.query(Uye).filter(Uye.uye_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('uye_guncelle_sil'))



# duyuru listeleme işlemleri yönetici
@app.route('/yonetici_duyuru_listesi')
def yonetici_duyuru_listesi():
    try:
        uye_id = session['yonetici']
        duyurular = Duyuru.query.all()
        return render_template("yonetici_duyuru_listesi.html", yonetici=kullanici['yonetici'], duyurular=duyurular)
    except:
        return render_template("yonetici_duyuru_listesi.html", yonetici=kullanici['yonetici'])

#duyuru ekleme işlemleri
@app.route('/yonetici_duyuru_ekle', methods=['GET', 'POST'])
@app.route('/yonetici_duyuru_ekle')
def yonetici_duyuru_ekle():
    tarih = datetime.today().utcnow()
    tarih = tarih.strftime("%d/%m/%Y")
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['duyuru_tarihi'], '%d/%m/%Y')
                tarih = datetime.date(tarih)
                yeni_duyuru = Duyuru(duyuru_yonetici_id=session['yonetici'],
                                   duyuru_basligi=bilgiler['duyuru_basligi'],
                                   duyuru_tarihi=tarih,
                                   duyuru_aciklama=bilgiler['duyuru_aciklama'])
                dbsession.add(yeni_duyuru)
                dbsession.commit()
                return render_template("yonetici_duyuru_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("yonetici_duyuru_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:
            return render_template("yonetici_duyuru_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)
    except:
        return render_template("yonetici_duyuru_ekle.html", yonetici=kullanici['yonetici'], tarih=tarih)


# duyuru güncelleme ve silme işlemleri
@app.route('/yonetici_duyuru_guncelle_sil/<int:id>')
@app.route('/yonetici_duyuru_guncelle_sil')
def yonetici_duyuru_guncelle_sil(id=0):
    if id == 0:
        duyurular = Duyuru.query.all()

        return render_template("yonetici_duyuru_guncelle_sil.html", yonetici=kullanici['yonetici'], duyurular=duyurular)
    else:
        return redirect(url_for('yonetici_duyuru_listesi'))

#yönetici bölümü duyuru güncelleme
@app.route('/yonetici_duyuru_guncelle/<int:id>')
@app.route('/yonetici_duyuru_guncelle', methods=['GET', 'POST'])
def yonetici_duyuru_guncelle(id=0):
    if id != 0:
        duyurular = Duyuru.query.filter_by(duyuru_id=id).first()
        return render_template("yonetici_duyuru_guncelle.html", yonetici=kullanici['yonetici'], duyurular=duyurular)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['duyuru_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        dbsession.query(Duyuru).filter(Duyuru.duyuru_id == bilgiler['duyuru_id']).update(
            {Duyuru.duyuru_basligi: bilgiler['duyuru_basligi'],
             Duyuru.duyuru_tarihi: tarih, Duyuru.duyuru_aciklama: bilgiler['duyuru_aciklama']})
        dbsession.commit()
        return redirect(url_for('yonetici_duyuru_guncelle_sil'))
    else:
        return redirect(url_for('yonetici_duyuru_guncelle'))

#yönetici bölümü duyuru goruntuleme
@app.route('/yonetici_duyuru_goruntuleme/<int:id>')
@app.route('/yonetici_duyuru_goruntuleme', methods=['GET', 'POST'])
def yonetici_duyuru_goruntuleme(id=0):
    if id != 0:
        duyurular = Duyuru.query.filter_by(duyuru_id=id).first()
        return render_template("yonetici_duyuru_goruntuleme.html", yonetici=kullanici['yonetici'], duyuru=duyurular)
    else:
        return redirect(url_for('yonetici_duyuru_listesi'))


#yönetici paneli duyuru silme bölümü
@app.route('/yonetici_duyuru_sil/<int:sil>')
def yonetici_duyuru_sil(sil=0):
    if sil != 0:
        dbsession.query(Duyuru).filter(Duyuru.duyuru_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('yonetici_duyuru_guncelle_sil'))


# yönetici istek işlemleri yönetici
@app.route('/yonetici_istek_listesi')
def yonetici_istek_listesi():
    try:
        uye_id = session['yonetici']
        istekler = Sikayet.query.all()
        return render_template("yonetici_istek_listesi.html", yonetici=kullanici['yonetici'], istekler=istekler)
    except:
        return render_template("yonetici_istek_listesi.html", yonetici=kullanici['yonetici'])

#yönetici bölümü istek goruntuleme
@app.route('/yonetici_istek_goruntuleme/<int:id>')
@app.route('/yonetici_istek_goruntuleme', methods=['GET', 'POST'])
def yonetici_istek_goruntuleme(id=0):
    if id != 0:
        istek = Sikayet.query.filter_by(sikayet_id=id).first()
        return render_template("yonetici_istek_goruntuleme.html", yonetici=kullanici['yonetici'], istek=istek)
    else:
        return redirect(url_for('yonetici_istek_listesi'))


#yönetici paneli istek silme bölümü
@app.route('/yonetici_istek_sil/<int:sil>')
def yonetici_istek_sil(sil=0):
    if sil != 0:
        dbsession.query(Sikayet).filter(Sikayet.sikayet_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('yonetici_istek_listesi'))

# duyuru listeleme işlemleri üye
@app.route('/uye_duyuru_listesi')
def uye_duyuru_listesi():
    try:
        uye_id = session['uye']
        duyurular = Duyuru.query.all()
        return render_template("uye_duyuru_listesi.html", uye=kullanici['uye'], duyurular=duyurular)
    except:
        return render_template("uye_duyuru_listesi.html", yonetici=kullanici['yonetici'])

#üye bölümü duyuru goruntuleme
@app.route('/uye_duyuru_goruntuleme/<int:id>')
@app.route('/uye_duyuru_goruntuleme', methods=['GET', 'POST'])
def uye_duyuru_goruntuleme(id=0):
    if id != 0:
        duyurular = Duyuru.query.filter_by(duyuru_id=id).first()
        return render_template("uye_duyuru_goruntuleme.html", uye=kullanici['uye'], duyuru=duyurular)
    else:
        return redirect(url_for('uye_duyuru_listesi'))


# üye istek işlemleri yönetici
@app.route('/uye_istek_listesi')
def uye_istek_listesi():
    try:
        uye_id = session['uye']
        istekler = Sikayet.query.filter_by(sikayet_uye_id=uye_id).all()
        return render_template("uye_istek_listesi.html", uye=kullanici['uye'], istekler=istekler)
    except:
        return render_template("uye_istek_listesi.html", uye=kullanici['uye'])

#üye bölümü istek goruntuleme
@app.route('/uye_istek_goruntuleme/<int:id>')
@app.route('/uye_istek_goruntuleme', methods=['GET', 'POST'])
def uye_istek_goruntuleme(id=0):
    if id != 0:
        uye_id = session['uye']
        istek = Sikayet.query.filter_by(sikayet_id=id, sikayet_uye_id=uye_id).first()
        return render_template("uye_istek_goruntuleme.html", uye=kullanici['uye'], istek=istek)
    else:
        return redirect(url_for('uye_istek_listesi'))

#uye paneli istek silme bölümü
@app.route('/uye_istek_sil/<int:sil>')
def uye_istek_sil(sil=0):
    if sil != 0:
        dbsession.query(Sikayet).filter(Sikayet.sikayet_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('uye_istek_listesi'))

#duyuru ekleme işlemleri üye
@app.route('/uye_istek_ekle', methods=['GET', 'POST'])
@app.route('/uye_istek_ekle')
def uye_istek_ekle():
    tarih = datetime.today().utcnow()
    tarih = tarih.strftime("%d/%m/%Y")
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['sikayet_tarihi'], '%d/%m/%Y')
                tarih = datetime.date(tarih)
                yeni_istek = Sikayet(sikayet_uye_id=session['uye'],
                                   sikayet_basligi=bilgiler['sikayet_basligi'],
                                   sikayet_tarihi=tarih,
                                   sikayet_aciklama=bilgiler['sikayet_aciklama'])
                dbsession.add(yeni_istek)
                dbsession.commit()
                return render_template("uye_istek_ekle.html", uye=kullanici['uye'], mesaj="Başarı")
            except:
                return render_template("uye_istek_ekle.html", uye=kullanici['uye'], mesaj="Başarısızlık")
        else:
            return render_template("uye_istek_ekle.html", uye=kullanici['uye'], tarih=tarih)
    except:
        return render_template("uye_istek_ekle.html", uye=kullanici['uye'], tarih=tarih)




def dernek_bilgisi():
    aidat_sayisi = db.session.query(Aidat).count()
    dernek_bilgileri['aidat_sayisi'] = aidat_sayisi
    aidat_toplami = db.session.query(Aidat, label('total_balance', func.sum(Aidat.aidat_tutari))).all()
    aidat_toplami = aidat_toplami[0][1]
    dernek_bilgileri['aidat_toplami'] = aidat_toplami

    bagis_sayisi = db.session.query(Bagis).count()
    dernek_bilgileri['bagis_sayisi'] = bagis_sayisi
    bagis_toplami = db.session.query(Bagis, label('total_balance', func.sum(Bagis.bagis_tutari))).all()
    bagis_toplami = bagis_toplami[0][1]
    dernek_bilgileri['bagis_toplami'] = bagis_toplami

    gider_sayisi = db.session.query(Gider).count()
    dernek_bilgileri['gider_sayisi'] = gider_sayisi
    gider_toplami = db.session.query(Gider, label('total_balance', func.sum(Gider.gider_tutari))).all()
    gider_toplami = gider_toplami[0][1]
    dernek_bilgileri['gider_toplami'] = gider_toplami

    auye_sayisi = db.session.query(Uye).filter(Uye.uye_durum == 0).count()
    dernek_bilgileri['auye_sayisi'] = auye_sayisi
    puye_sayisi = db.session.query(Uye).filter(Uye.uye_durum == 1).count()
    dernek_bilgileri['puye_sayisi'] = puye_sayisi
    tuye_sayisi = db.session.query(Uye).count()
    dernek_bilgileri['tuye_sayisi'] = tuye_sayisi
    return dernek_bilgileri


if __name__ == '__main__':
    app.run(debug=True)
