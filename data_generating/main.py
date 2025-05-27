import random
import pandas as pd
from faker import Faker
from datetime import datetime, date
import csv

fake = Faker()

hesab_novleri = ["Əmanət", "Cari", "Biznes", "Depozit"]
filiallar = ["Bakı", "Gəncə", "Sumqayıt", "Şəki", "Lənkəran", "Mingəçevir", "Naxçıvan", "Qax", "Zaqatala", "Quba", "Qusar"]
olke = "Azərbaycan"
email_domain = "@gmail.com"

female_first_names = [
    "Aysel", "Ləman", "Nigar", "Zəhra", "Sevinc",
    "Günay", "Fidan", "Şəbnəm", "Aytən", "Kəmalə",
    "Ülviyyə", "Gülşən", "Lətafət", "Xuraman", "Səbinə"
]

female_last_names = [
    "Rzayeva", "Axundova", "Məmmədova", "Əliyeva", "Qasımova",
    "Hüseynova", "Əlizadə", "İsmayılova", "Nəbiyeva", "Cəfərova",
    "Orucova", "Bədəlova", "Hacıyeva", "Ələkbərova", "Mürsəlova"
]

male_first_names = [
    "Elvin", "Murad", "Rauf", "Tural", "Nihat",
    "Cavid", "Emil", "Anar", "Orxan", "Şahin",
    "Nicat", "Elnur", "İlkin", "Kənan", "Kamran",
    "Qurban","Fərid","Əli"
]

male_last_names = [
    "Məmmədov", "Əliyev", "Hüseynov", "Quliyev", "İsmayılov",
    "Əlizadə", "Axundov", "Qasımov", "Nəbiyev", "Cəfərov",
    "Orucov", "Bədəlov", "Hacıyev", "Ələkbərov", "Mürsəlov",
    "Vəliyev","Mahmudov"
]

def musteri_yarat(i):
    cins = random.choice(["Kişi", "Qadın"])
    if cins == "Qadın":
        ad = random.choice(female_first_names)
        soyad = random.choice(female_last_names)
    else:
        ad = random.choice(male_first_names)
        soyad = random.choice(male_last_names)

    ad_soyad = f"{ad} {soyad}"
    email = ad_soyad.lower().replace(" ", ".") + str(random.randint(1, 99)) + email_domain
    telefon = "+994" + str(random.randint(50, 55)) + str(random.randint(1000000, 9999999))
    yas = random.randint(18, 75)
    
    max_tenure = min(yas - 18, 10)
    tenure = random.randint(0, max(0, max_tenure))
    
    ayliq_gelir = round(random.uniform(300, 10000), 2)
    kredit_reytinqi = random.randint(300, 850)
    
    # kredit_uygundur check
    kredit_uygundur = ayliq_gelir > 2000 and kredit_reytinqi > 650 and yas >= 21

    # hesab_novu based on income
    if ayliq_gelir > 5000:
        hesab_novu = random.choices(["Biznes", "Depozit"], weights=[0.6, 0.4])[0]
    else:
        hesab_novu = random.choices(["Əmanət", "Cari"], weights=[0.5, 0.5])[0]

    # balans based on income and tenure
    base_balans = ayliq_gelir * random.uniform(0.5, 2)
    balans = round(base_balans * (1 + tenure / 10), 2)

    # num_of_products based on tenure
    if tenure < 2:
        num_of_products = random.randint(1, 2)
    elif tenure < 5:
        num_of_products = random.randint(1, 3)
    else:
        num_of_products = random.randint(2, 4)

    # credit card likelihood based on income
    has_credit_card = int(random.random() < (0.7 if ayliq_gelir > 1500 else 0.3))

    # estimated salary
    estimated_salary = round(random.uniform(1000, 20000), 2)

    # churn probability
    churn_prob = (
        0.3 * (tenure < 3) +
        0.2 * (kredit_reytinqi < 600) +
        0.2 * (num_of_products == 1)
    )
    churn = int(random.random() < churn_prob)

    # is_active_member check
    is_active_member = 0 if churn else random.choice([0, 1])
    
    # yaradilma_tarixi based on tenure
    this_year = datetime.now().year
    try:
        yaradilma_tarixi = date(this_year - tenure, random.randint(1, 12), random.randint(1, 28)).isoformat()
    except ValueError:
        yaradilma_tarixi = fake.date_between(start_date='-10y', end_date='-1y').isoformat()

    return {
        "customer_id": f"MST{i:05d}",
        "name_surname": ad_soyad,           # name_surname (full name)
        "age": yas,                        # age
        "gender": cins,                   # gender
        "email": email,                   # email
        "phone": telefon,                 # phone
        "account_type": hesab_novu,       # account_type
        "balance": balans,                # balance
        "branch": random.choice(filiallar),  # branch
        "credit_rating": kredit_reytinqi,    # credit_rating (credit score)
        "is_active": bool(is_active_member),  # is_active
        "last_transaction_date": fake.date_between(start_date='-1y', end_date='today').isoformat(),  # last_transaction_date
        "monthly_income": ayliq_gelir,            # monthly_income
        "credit_eligible": kredit_uygundur,       # credit_eligible
        "country": olke,                           # country
        "account_creation_date": yaradilma_tarixi, # account_creation_date
        "tenure": tenure,                          # tenure (how long customer has been with bank)
        "num_of_products": num_of_products,       # number_of_products
        "has_credit_card": has_credit_card,       # has_credit_card (0/1)
        "is_active_member": is_active_member,     # is_active_member (0/1)
        "estimated_salary": estimated_salary,     # estimated_salary
        "churn": churn                            # churn (0 = stayed, 1 = left)
}

with open("Azerbaijan_bank_customers.csv", "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = list(musteri_yarat(0).keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(20000):
        writer.writerow(musteri_yarat(i))

print("✅ 20,000 nəfərlik Azərbaycan bank datası (churn modelləşdirmə üçün) yaradıldı və fayla yazıldı.")