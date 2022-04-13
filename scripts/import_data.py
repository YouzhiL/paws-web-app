import csv
from main.models import CustomUser, Category, ProductFB, SellerFB, General_Product, Product, OrderItem, Order, Address, Coupon

def run():
    
    with open("/Users/tl/Desktop/paws-web-app-main/data/customuser.csv") as file_customuser:
        reader1 = csv.reader(file_customuser)

        CustomUser.objects.all().delete()

        for row in reader1:
            customuser = CustomUser(
                username = row[0],
                first_name = row[1],
                last_name = row[2],
                password = row[3],
                mailing_address = row[4],
                email = row[5],
                balance = row[6],
                is_seller = row[7],
            )
            customuser.save()

    with open("/Users/tl/Desktop/paws-web-app-main/data/category.csv") as file_category:
        reader2 = csv.reader(file_category)

        Category.objects.all().delete()

        for row in reader2:
            category = Category(
                name = row[0]
            )
            category.save()
    
    with open("/Users/tl/Desktop/paws-web-app-main/data/productfb.csv") as file_productfb:
        reader3 = csv.reader(file_productfb)

        ProductFB.objects.all().delete()

        for row in reader3:
            user,_ = CustomUser.objects.get_or_create(username=row[0])
            productfb = ProductFB(
               user = user,
               rating = row[1],
               review = row[2],  
               helpful = row[3],
               date = row[5]
            )
            productfb.save()

            upvoteby_list = CustomUser.objects.filter(username=row[4])    
            for upvoteby in upvoteby_list:
                productfb.upvoteby.add(upvoteby)

    with open("/Users/tl/Desktop/paws-web-app-main/data/sellerfb.csv") as file_sellerfb:
        reader4 = csv.reader(file_sellerfb)

        SellerFB.objects.all().delete()

        for row in reader4:
            user,_ = CustomUser.objects.get_or_create(username=row[0])
            seller,_ = CustomUser.objects.get_or_create(username=row[1])
            
            sellerfb = SellerFB(
               user = user,
               seller = seller,
               rating = row[2],
               review = row[3],  
               helpful = row[4],
               date = row[5]
            )
            sellerfb.save()

    with open("/Users/tl/Desktop/paws-web-app-main/data/generalpd.csv") as file_generalpd:
        reader5 = csv.reader(file_generalpd)
        General_Product.objects.all().delete()
        Category.objects.all().delete()

        for row in reader5:
            category, _ = Category.objects.get_or_create(name=row[2])

            generalpd = General_Product(
               product_name = row[0],
               product_img = row[1],
               category = category,
               description = row[3],
               slug = row[4]
            )
            generalpd.save()

            fb_list = ProductFB.objects.filter(rating=row[5])    
            for feedback in fb_list:
                generalpd.feedback.add(feedback)

    with open("/Users/tl/Desktop/paws-web-app-main/data/product.csv") as file_product:
        reader6 = csv.reader(file_product)
    
        Product.objects.all().delete()
        
        for row in reader6:
            general_product, _ = General_Product.objects.get_or_create(product_name=row[0])
            seller, _ = CustomUser.objects.get_or_create(username=row[4])
    
            product = Product(
                general_product = general_product,
                price = row[1],
                discount_price = row[2],
                quantity = row[3],
                seller = seller,
                slug = row[5]           
            )
            product.save()
            

    