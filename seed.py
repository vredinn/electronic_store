import datetime
from sqlalchemy.orm import Session
from database import engine, Base
from security import get_password_hash
from models import (
    User,
    Category,
    Product,
    Order,
    OrderItem,
    Review,
    UserRole,
    OrderStatus,
    ReviewStatus,
)


def seed_data():
    print("Очистка базы данных...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = Session(bind=engine)

    print("База данных очищена и создана заново.")
    print("Загрузка данных в базу данных...")

    try:

        # Пользователи
        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("AdminPass123!"),
                role=UserRole.ADMIN,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            User(
                username="manager1",
                email="manager1@example.com",
                hashed_password=get_password_hash("ManagerPass123!"),
                role=UserRole.MANAGER,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            User(
                username="manager2",
                email="manager2@example.com",
                hashed_password=get_password_hash("ManagerPass456!"),
                role=UserRole.MANAGER,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            User(
                username="buyer1",
                email="buyer1@example.com",
                hashed_password=get_password_hash("BuyerPass123!"),
                role=UserRole.BUYER,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            User(
                username="buyer2",
                email="buyer2@example.com",
                hashed_password=get_password_hash("BuyerPass456!"),
                role=UserRole.BUYER,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            User(
                username="buyer3",
                email="buyer3@example.com",
                hashed_password=get_password_hash("BuyerPass789!"),
                role=UserRole.BUYER,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
        ]
        db.add_all(users)
        db.commit()

        # Категории
        categories = [
            Category(
                name="Смартфоны",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
            Category(
                name="Ноутбуки",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
            Category(
                name="Планшеты",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
            Category(
                name="Наушники",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
            Category(
                name="Умные часы",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
            Category(
                name="Телевизоры",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            ),
        ]
        db.add_all(categories)
        db.commit()

        # Продукты
        products = [
            Product(
                name="iPhone 15 Pro",
                price=99990,
                category_id=1,
                description="Флагманский смартфон от Apple",
                stock=50,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Samsung Galaxy S23 Ultra",
                price=119990,
                category_id=1,
                description="Флагманский смартфон от Samsung",
                stock=40,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Xiaomi Redmi Note 12 Pro",
                price=29990,
                category_id=1,
                description="Популярный смартфон с хорошей камерой",
                stock=60,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name='MacBook Pro 16" M2',
                price=249990,
                category_id=2,
                description="Мощный ноутбук для профессионалов",
                stock=25,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Dell XPS 15",
                price=199990,
                category_id=2,
                description="Премиальный ноутбук с безрамочным дисплеем",
                stock=30,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Asus VivoBook 15",
                price=59990,
                category_id=2,
                description="Бюджетный ноутбук для повседневных задач",
                stock=40,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name='iPad Pro 12.9"',
                price=109990,
                category_id=3,
                description="Мощный планшет от Apple",
                stock=35,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Samsung Galaxy Tab S8 Ultra",
                price=99990,
                category_id=3,
                description="Флагманский планшет от Samsung",
                stock=20,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Sony WH-1000XM5",
                price=39990,
                category_id=4,
                description="Беспроводные наушники с шумоподавлением",
                stock=60,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Apple AirPods Pro 2",
                price=24990,
                category_id=4,
                description="Беспроводные наушники от Apple",
                stock=50,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Apple Watch Series 8",
                price=42990,
                category_id=5,
                description="Умные часы от Apple",
                stock=45,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Samsung Galaxy Watch 5",
                price=29990,
                category_id=5,
                description="Умные часы от Samsung",
                stock=35,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="LG OLED C2",
                price=179990,
                category_id=6,
                description="55-дюймовый OLED телевизор",
                stock=15,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
            Product(
                name="Samsung QLED Q70A",
                price=99990,
                category_id=6,
                description="55-дюймовый QLED телевизор",
                stock=20,
                created_at=datetime.datetime.now() - datetime.timedelta(days=20),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=19),
            ),
        ]
        db.add_all(products)
        db.commit()

        # Заказы
        orders = [
            Order(
                user_id=4,  # buyer1
                status=OrderStatus.DELIVERED,
                amount=0,  # Будет рассчитано после добавления товаров
                created_at=datetime.datetime.now() - datetime.timedelta(days=15),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=10),
            ),
            Order(
                user_id=4,  # buyer1
                status=OrderStatus.PROCESSING,
                amount=0,
                created_at=datetime.datetime.now() - datetime.timedelta(days=10),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=5),
            ),
            Order(
                user_id=5,  # buyer2
                status=OrderStatus.SHIPPED,
                amount=0,
                created_at=datetime.datetime.now() - datetime.timedelta(days=8),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=3),
            ),
            Order(
                user_id=6,  # buyer3
                status=OrderStatus.PENDING,
                amount=0,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=2),
            ),
            Order(
                user_id=5,  # buyer2
                status=OrderStatus.DELIVERED,
                amount=0,
                created_at=datetime.datetime.now() - datetime.timedelta(days=12),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=7),
            ),
        ]
        db.add_all(orders)
        db.commit()

        # Товары в заказах
        order_items = [
            # Заказ 1 - 1 товар
            OrderItem(
                order_id=1,
                product_id=1,  # iPhone 15 Pro
                quantity=1,
                price_at_order=products[0].price,
            ),
            # Заказ 2 - 2 товара
            OrderItem(
                order_id=2,
                product_id=3,  # Xiaomi Redmi Note 12 Pro
                quantity=1,
                price_at_order=products[2].price,
            ),
            OrderItem(
                order_id=2,
                product_id=9,  # Sony WH-1000XM5
                quantity=2,
                price_at_order=products[8].price,
            ),
            # Заказ 3 - 1 товар (2 штуки)
            OrderItem(
                order_id=3,
                product_id=2,  # Samsung Galaxy S23 Ultra
                quantity=2,
                price_at_order=products[1].price,
            ),
            # Заказ 4 - 2 товара
            OrderItem(
                order_id=4,
                product_id=7,  # iPad Pro 12.9"
                quantity=1,
                price_at_order=products[6].price,
            ),
            OrderItem(
                order_id=4,
                product_id=10,  # Apple AirPods Pro 2
                quantity=1,
                price_at_order=products[9].price,
            ),
            # Заказ 5 - 1 товар
            OrderItem(
                order_id=5,
                product_id=13,  # LG OLED C2
                quantity=1,
                price_at_order=products[12].price,
            ),
        ]
        db.add_all(order_items)
        db.commit()

        # Обновление сумм заказов
        for order in orders:
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            order.amount = sum(item.price_at_order * item.quantity for item in items)
        db.commit()

        # Отзывы
        reviews = [
            Review(
                product_id=1,  # iPhone 15 Pro
                user_id=4,  # buyer1
                rating=5,
                text="Отличный телефон! Камера просто супер.",
                status=ReviewStatus.APPROVED,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=4),
            ),
            Review(
                product_id=2,  # Samsung Galaxy S23 Ultra
                user_id=5,  # buyer2
                rating=4,
                text="Хороший телефон, но дорогой",
                status=ReviewStatus.APPROVED,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=4),
            ),
            Review(
                product_id=3,  # Xiaomi Redmi Note 12 Pro
                user_id=6,  # buyer3
                rating=5,
                text="Отличное соотношение цены и качества!",
                status=ReviewStatus.PENDING,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=4),
            ),
            Review(
                product_id=7,  # iPad Pro 12.9"
                user_id=4,  # buyer1
                rating=5,
                text="Лучший планшет на рынке!",
                status=ReviewStatus.APPROVED,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=4),
            ),
            Review(
                product_id=9,  # Sony WH-1000XM5
                user_id=5,  # buyer2
                rating=3,
                text="Хорошие наушники, но неудобные для долгого ношения",
                status=ReviewStatus.PENDING,
                created_at=datetime.datetime.now() - datetime.timedelta(days=5),
                updated_at=datetime.datetime.now() - datetime.timedelta(days=4),
            ),
        ]
        db.add_all(reviews)
        db.commit()

        print("Данные успешно загружены.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
