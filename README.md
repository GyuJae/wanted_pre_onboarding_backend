<h1> Wanted Pre Onboarding</h1>

## 구현 과정

### 상품 model 설정

core_models.TimeStampedModel에 created_at, updated_at를 설정하여 상속받음.

model method를 이용하여 게시자명, 달성률, D-day(펀딩 종료일까지), 참여자 수 작성.

참여자들은 ManyToManyField 사용

```
    class Product(core_models.TimeStampedModel):

    """Product Model Definition"""

    title = models.CharField(max_length=140)
    publisher = models.ForeignKey(
        "users.User", related_name="products", on_delete=models.CASCADE
    )

    description = models.TextField()
    target_amount = models.IntegerField()
    funding_end_date = models.DateField()
    one_time_funding_amount = models.IntegerField()
    total_amount = models.IntegerField(default=0)
    participants = models.ManyToManyField("users.User")

    def __str__(self):
        return self.title

    def publisher_name(self):
        return self.publisher.username

    def participants_count(self):
        return self.participants.count()

    def d_day(self):

        import datetime

        today = datetime.date.today()
        end_date_split = list(map(int, str(self.funding_end_date).split("-")))
        target_date = datetime.date(
            end_date_split[0], end_date_split[1], end_date_split[2]
        )
        return (target_date - today).days

    def achievment_rate(self):
        return self.total_amount / self.target_amount
```

### Views 구현

APIView class 사용

permission_classes를 설정하여 상품등록 Authorization 부여

```
    class ProductList(APIView):

    """List all products, or creat e a new product"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(sef, request, format=None):
        if request.query_params.get("search"):
            keyword = request.query_params.get("search")
            products = Product.objects.filter(title__contains=keyword)
        elif request.query_params.get("order_by"):
            order_keyword = request.query_params.get("order_by")
            if order_keyword == "생성일":
                products = Product.objects.all().order_by("-created_at")
            elif order_keyword == "총펀딩금액":
                products = Product.objects.all().order_by("-total_amount")
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        data["publisher"] = request.user.id
        serializer = CreateProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

자신의 product만 update 및 delete method 사용가능

```
    if product.publisher_name() != request.user.username:
        return Response(
                {"details": "not your product"}, status=status.HTTP_401_UNAUTHORIZED
        )
```

```
    class ProductDetail(APIView):

    """
    Retrieve, update or delete a code product.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        if product.publisher_name() != request.user.username:
            return Response(
                {"details": "not your product"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UpdateProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if product.publisher_name() != request.user.username:
            return Response(
                {"details": "not your product"}, status=status.HTTP_401_UNAUTHORIZED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

1회 펀딩 참여시 총펀딩금액에 상품의 1회펀딩금액만큼 증가
처음 펀딩 참여한 유저는 상품 참여자에 추가됨

```
    class ProductFunding(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        product.participants.add(request.user)
        product.total_amount += product.one_time_funding_amount
        product.save()
        return Response(status=status.HTTP_200_OK)
```

### Serializers

serializer를 이용하여 data 설정함.

#### CreateProductSerializer

제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액으로 구성

```
    class CreateProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = [
                "title",
                "description",
                "target_amount",
                "funding_end_date",
                "one_time_funding_amount",
                "publisher",
            ]
```

#### UpdateProductSerializer

모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다. -> CreateProductSerializer fields에서 target_amount 제거

```
    class UpdateProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = [
                "title",
                "description",
                "funding_end_date",
                "one_time_funding_amount",
            ]
```

#### ProductSerializer

제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액 및 참여자 수 가 포함되어야 합니다.

```
    class ProductSerializer(serializers.ModelSerializer):

    d_day = serializers.SerializerMethodField()
    achievment_rate = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "publisher_name",
            "description",
            "target_amount",
            "funding_end_date",
            "one_time_funding_amount",
            "d_day",
            "achievment_rate",
            "total_amount",
            "participants_count",
        ]

    def d_day(self, instance):
        return instance.d_day()

    def achievment_rate(self, instance):
        return instance.achievment_rate()

    def participants_count(self, instance):
        return instance.participants_count()
```

### Unit Test

APITestCase를 unit test case 작성 -> User and Product app test class 작성 (총 27 테스트)

ex)

```
    class TestProductLists(APITestCase):

    url = "/products/"

    def setUp(self) -> None:
        self.user = User.objects.create(
            username="test_user", password="1", email="test@test.com"
        )
        self.client.force_authenticate(user=self.user)
        Product.objects.create(
            title="test product",
            description="this is test product",
            target_amount=1000,
            funding_end_date="2022-04-20",
            one_time_funding_amount=200,
            publisher=self.user,
        )
        Product.objects.create(
            title="product2",
            description="this is test product2",
            target_amount=1000,
            funding_end_date="2022-04-20",
            one_time_funding_amount=2000,
            publisher=self.user,
            total_amount=100,
        )

    def test_get_search_products(self):
        search_url = "/products/?search=test"
        response = self.client.get(search_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "test product")
        self.assertEqual(len(result), 1)

    def test_get_order_by_created_at_products(self):
        order_by_url = "/products/?order_by=생성일"
        response = self.client.get(order_by_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "product2")
        self.assertEqual(len(result), 2)

    def test_get_order_by_total_amount_products(self):
        order_by_url = "/products/?order_by=총펀딩금액"
        response = self.client.get(order_by_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "product2")
        self.assertEqual(len(result), 2)

    def test_get_products(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "test product")
        self.assertEqual(len(result), 2)

    def test_post_serializer_error_product(self):
        data = {
            "title": "new product",
            "description": "this is new product",
            "target_amount": 1000,
            "funding_end_date": "2022-04-22",
        }

        response = self.client.post(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["one_time_funding_amount"], ["This field is required."])

    def test_post_product(self):
        data = {
            "title": "new product",
            "description": "this is new product",
            "target_amount": 1000,
            "funding_end_date": "2022-04-22",
            "one_time_funding_amount": 200,
        }

        response = self.client.post(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["title"], "new product")

```
