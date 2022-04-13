import csv
from faker import Faker
from werkzeug.security import generate_password_hash
from datetime import datetime
import string
import random

num_users = 1000
num_products = 1000
num_order = 1000
num_coupon = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_address(num_users):
    apartment_list = []
    street_list = []
    state_list = []
    zip_list = []
    with open('/Users/tl/Desktop/paws-web-app/data/address.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            apartment = fake.building_number()
            apartment_list.append(apartment)
            street = fake.street_address()
            street_list.append(street)
            state = fake.state_abbr()
            state_list.append(state)
            zip = fake.postcode()
            zip_list.append(zip)
            address_type = fake.random_element(elements=('resident address', 'current address'))
            default = fake.random_int(min=0, max=1)
            writer.writerow([apartment, street, state, zip, address_type, default])
    return apartment_list, street_list, state_list, zip_list


def gen_users(num_users, apartment_list, street_list, state_list, zip_list):
    name_list = []
    seller_list =[]
    address_list = []
    email_list = []
    with open('/Users/tl/Desktop/paws-web-app/data/customuser.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            profile = fake.profile()
            address = f'Apt {apartment_list[uid]}, {street_list[uid]}, {state_list[uid]} {zip_list[uid]}'
            address_list.append(address)
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = fake.unique.name()
            first_name = name_components.split(' ')[0]
            last_name = name_components.split(' ')[1]
            name_list.append(name_components)
            email = profile['mail']
            email_list.append(email)
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            is_seller = fake.random_int(min=0, max=1)
            if is_seller == 1:
                seller_list.append(name_components)
            writer.writerow([name_components, first_name, last_name, password, address, email, balance, is_seller])
    return name_list, seller_list, address_list, email_list

def gen_category(num_products):
    category_list = []
    with open('/Users/tl/Desktop/paws-web-app/data/category.csv', 'w') as f:
        writer = get_csv_writer(f)
        for pid in range(num_users):
            name = fake.random_element(elements=('food', 'toys', 'treats', 'beds'))
            category_list.append(name)
            writer.writerow([name])
    return category_list

def gen_productfb(num_users, name_list):
    with open('/Users/tl/Desktop/paws-web-app/data/productfb.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            user = fake.random_element(elements=name_list)  
            rating = fake.random_int(min=1, max=5)
            if rating >= 4:
                review = fake.random_element(elements=('excellent', 'good'))
            elif rating >= 2:
                review = fake.random_element(elements=('average', 'not recommended'))
            else:
                review = 'bad'
            helpful = fake.random_int(min=1, max=5)
            upvoteby = fake.random_element(elements=name_list)
            date = fake.date_time()
            writer.writerow([user, rating, review, helpful, upvoteby, date])
    return

def gen_sellerfb(num_users, seller_list):
    with open('/Users/tl/Desktop/paws-web-app/data/sellerfb.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            user = fake.random_element(elements=name_list)
            seller = fake.random_element(elements=seller_list)
            rating = fake.random_int(min=1, max=5)
            if rating >= 4:
                review = fake.random_element(elements=('excellent', 'good'))
            elif rating >= 2:
                review = fake.random_element(elements=('average', 'not recommended'))
            else:
                review = 'bad'
            helpful = fake.random_int(min=1, max=5)
            date = fake.date_time_between(start_date=datetime(2016,1,1,0,0,0))
            writer.writerow([user, seller, rating, review, helpful, date])
    return

def gen_generalpd(num_products, category_list):
    pd_name_list = []
    with open('/Users/tl/Desktop/paws-web-app/data/generalpd.csv', 'w') as f:
        writer = get_csv_writer(f)
        for pid in range(num_products):
            # rand_name = fake.sentence(nb_words=4)[:-1]
            cat = fake.random_element(elements=('food', 'toys', 'treats', 'beds'))
            product_name = f'{cat}: {pid}'
            pd_name_list.append(product_name)
            if cat == 'food':
                product_img = 'https://cdn.shopify.com/s/files/1/0593/6273/8342/products/PDP_Cat_SALMON_02_Bowl_548x768_crop_center_7390be29-b4b0-4f7e-a633-4365a84690d1_1200x1200.png?v=1646504820'
                description = fake.random_element(elements=('Sustainably raised salmon is the #1 ingredient; protein helps keep dogs at their bounding best.', 'NO ADDED SALMON BY-PRODUCT MEAL, corn, wheat, soy, artificial colors, flavors, or preservatives.', 'This natural dog food grain free recipe contains 65% protein and healthy fat ingredients, and 35% produce, fiber, vitamins, minerals and other natural ingredients.'))
            elif cat == 'toys':
                product_img = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/indoor-dog-toys-1587002073.jpg?crop=1.00xw:0.751xh;0,0.161xh&resize=1200:*'
                description = fake.random_element(elements=('Our dog toys are made of natural and non-toxic material that ensures the safety of dogs. Thicker fabric and better stitching make these toys more durable for dogs. It is suitable for teeth cleaning and chewing.', 'Squeeky sound, fetchable, chewable, tossable and 12 tiny dog toys to play, entice your dog to run, chase and exercise, great bulk dog toys for boredom, reduce anxiety and give them mental and physical workout.', 'High Quality & Excellence Service: Our dog chew toys undergo rigorous quality testing. Made of durable and natural material, good for dogs. Feel free to contact us if you have any questions. Our friendly support team is always here to help you. You can confidently buy our products, this dog toy pack is definitely a good choice for you.'))
            elif cat == 'treats':
                product_img = 'https://www.petfoodindustry.com/ext/resources/Images-by-month-year/18_03/Dog-treats-chews.jpg?t=1526243719&width=1080'
                description = fake.random_element(elements=('Real salmon is the #1 ingredient. Crunchy texture helps clean teeth.', 'No artificial flavors or colors. Innovative design with a chewy, porous texture.', 'Soft and chewy dog treats made with real chuck roast. Fortified with 12 vitamins and minerals.'))
            else:
                product_img = 'https://assets.pbimgs.com/pbimgs/rk/images/dp/wcm/202212/0013/3-in-1-pet-bed-z.jpg'
                description = fake.random_element(elements=('ASSORTED SIZE: X-Large -- 32''x24''x8'' donut bed perfect for your cat, small or medium dogs weight up to 35lbs. Our calming bed not suitable for puppies or dogs with excessive teething or chewing behavior!', 'High quality soft faux fur surface material feels like mommy s fur, provide a warmth and safety, comfortable quality sleeping environment for pets. It helps them to calm down faster, ease anxiety, and sleep well.', 'The sleep surface (28”x23”) is made of a flannel cover that provides a soft and comfortable sleeping area for dogs or cats.'))
            # category = fake.random_element(elements=category_list)
            slug = fake.sha256(raw_output=False)
            feedback = fake.random_int(min=1, max=5)
            writer.writerow([product_name, product_img, cat, description, slug, feedback])
    return pd_name_list

def gen_products(num_products, pd_name_list, seller_list):
    with open('/Users/tl/Desktop/paws-web-app/data/product.csv', 'w') as f:
        writer = get_csv_writer(f)
        for pid in range(num_products):
            general_pd = pd_name_list[pid]
            price = f'{str(fake.random_int(min=15, max=100))}.{fake.random_int(max=99):02}'
            discount_price = round(0.8 * float(price), 2)
            quantity = fake.random_int(min=30, max=200)
            seller = fake.random_element(elements=seller_list)
            slug = fake.sha256(raw_output=False)
            writer.writerow([general_pd, price, discount_price, quantity, seller, slug])
    return

def gen_orderitem(num_order, name_list, pd_name_list):
    with open('/Users/tl/Desktop/paws-web-app/data/orderitem.csv', 'w') as f:
        writer = get_csv_writer(f)
        for oid in range(num_order):
            user = fake.random_element(elements=name_list)
            ordered = fake.random_int(min=0, max=1)
            fullfilled = fake.random_int(min=0, max=1)
            fulfill_date = fake.date_time_between(start_date=datetime(2016,1,1,0,0,0))
            product = fake.random_element(elements=pd_name_list)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([user, ordered, fullfilled, fulfill_date, product, quantity])
    return

def gen_coupon(num_coupon):
    coupon_list = []
    with open('/Users/tl/Desktop/paws-web-app/data/coupon.csv', 'w') as f:
        writer = get_csv_writer(f)
        for i in range(num_coupon):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            coupon_list.append(code)
            amount = fake.random_int(min=300, max=500)
            writer.writerow([code, amount])
    return coupon_list


def gen_order(num_order, name_list, pd_name_list, address_list, coupon_list):
    with open('/Users/tl/Desktop/paws-web-app/data/order.csv', 'w') as f:
        writer = get_csv_writer(f)
        for oid in range(num_order):
            user = fake.random_element(elements=name_list)
            ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            items = fake.random_element(elements=pd_name_list)
            f = Faker()
            start_d = fake.date_time_between(start_date=datetime(2016,1,1,0,0,0))
            ordered_date = fake.date_time_between(start_date=datetime(2016,1,1,0,0,0))
            ordered = fake.random_int(min=0, max=1)
            shipping_address = fake.random_element(elements=address_list)
            billing_address = shipping_address
            coupon = fake.random_element(elements=coupon_list)
            fulfilled = fake.random_int(min=0, max=1)
            being_delivered = fake.random_int(min=0, max=1)
            received = fake.random_int(min=0, max=1)
            refund_requested = fake.random_int(min=0, max=1)
            refund_granted = fake.random_int(min=0, max=1)
            slug = fake.random_int(min=0, max=1)
            writer.writerow([user, ref_code, items, start_d, ordered_date, ordered, shipping_address, billing_address, coupon, fulfilled, being_delivered, received, refund_requested, refund_granted, slug])
    return

def gen_payment(num_order, name_list):
    with open('/Users/tl/Desktop/paws-web-app/data/payment.csv', 'w') as f:
        writer = get_csv_writer(f)
        for oid in range(num_order):
            stripe_charge_id = ''.join(random.choices(string.digits, k=12))
            user = fake.random_element(elements=name_list)
            amount = f'{str(fake.random_int(min=15, max=100))}.{fake.random_int(max=99):02}'
            timestamp = fake.date_time()
            writer.writerow([stripe_charge_id, user, amount, timestamp])
    return

def gen_refund(num_order, pd_name_list, email_list):
    with open('/Users/tl/Desktop/paws-web-app/data/refund.csv', 'w') as f:
        writer = get_csv_writer(f)
        for oid in range(num_order):
            order = fake.random_element(elements=pd_name_list)
            reason = fake.sentence(nb_words=10)[:-1]
            accepted = fake.random_int(min=0, max=1)
            email = fake.random_element(elements=email_list)
            writer.writerow([order, reason, accepted, email])
    return

def gen_cart(num_users, name_list, pd_name_list):
    with open('/Users/tl/Desktop/paws-web-app/data/refund.csv', 'w') as f:
        writer = get_csv_writer(f)
        for uid in range(num_users):
            user = fake.random_element(elements=name_list)
            product = fake.random_element(elements=pd_name_list)
            quantity = fake.random_int(min=0, max=10)
            writer.writerow([user, product, quantity])
    return

apartment_list, street_list, state_list, zip_list =gen_address(num_users)
name_list, seller_list, address_list, email_list = gen_users(num_users, apartment_list, street_list, state_list, zip_list)
category_list = gen_category(num_products)
gen_productfb(num_users, name_list)
gen_sellerfb(num_users, seller_list)
pd_name_list = gen_generalpd(num_products, category_list)
gen_products(num_products, pd_name_list, seller_list) 
gen_orderitem(num_order, name_list, pd_name_list)
coupon_list = gen_coupon(num_coupon)
gen_order(num_order, name_list, pd_name_list, address_list, coupon_list)
gen_payment(num_order, name_list)
gen_refund(num_order, pd_name_list, email_list)
gen_cart(num_users, name_list, pd_name_list)
