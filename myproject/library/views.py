from random import randint
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from .permissions import IsEmployer, IsClient
from .serializers import *
from django.db.models import Count, F
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BookIssue


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            client = Client.objects.create(user=user)
            client_serializer = ClientSerializer(client)
            return Response(client_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSetForEmployer(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]


class BookIssueView(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    @action(detail=True, methods=['post', 'get'])
    def return_book(self, request, pk=None):
        bookissue = self.get_object()
        book = bookissue.book
        client = bookissue.client
        if book.reserved_quantity == 0:
            return Response({'status': 'Book is not issued'}, status=400)
        book.reserved_quantity -= 1
        book.stock_quantity += 1
        book.save()
        book_issue = BookIssue.objects.filter(book=book, returned_at__isnull=True).first()
        if book_issue:
            book_issue.returned_at = datetime.now() - \
                                     timedelta(hours=4)  # აქ 4 აკლდება, რადგან ადმინის სერვერის დრო 4 საათით უკანაა,
            # ვიდრე ჩვენი დრო
            book_issue.save()
        else:
            return Response({'status': 'No book issue found'}, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            'status': 'Book returned',
            'book': book.title,
            'client': client.user.username
        }
        return Response(response_data)


class BookViewSetForClient(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsClient]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'authors__name', 'genres__name', 'publication_date']
    search_fields = ['title', 'authors__name', 'genres__name']
    ordering_fields = ['title', 'publication_date', 'stock_quantity', 'all_reserved_quantity']

    @action(detail=True, methods=['post', 'get'])
    def reserve(self, request, pk=None):
        book = self.get_object()
        client = Client.objects.get(user=request.user)
        if book.stock_quantity == 0:
            return Response({'status': 'Book is out of stock'}, status=400)
        if book.stock_quantity > 0:
            book.all_reserved_quantity += 1
            book.stock_quantity -= 1
            book.reserved_quantity += 1
            reservation = Reservation.objects.create(book=book, client=client)
            BookIssue.objects.create(book=book, client=client, issued_at=reservation.reserved_at + \
                                                                         timedelta(hours=randint(1, 20)), # აქ იგივე, დროის სხვაობის,
                                     # მიზეზის გამო ემატება 20 და არა 24 საათი
                                     have_to_return_at=reservation.reserved_at + \
                                                       timedelta(days=14)) # კლიენტებს აქვთ 14 დღე რომ დააბრუნონ წიგნი
            book.save()
            return Response({'status': 'Book reserved', 'reservation_id': reservation.id})

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# views.py


class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def popular_books(self, request):
        popular_books = Book.objects.order_by('-all_reserved_quantity')[:10]
        serializer = PopularBookSerializer(popular_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def book_issue_count_last_year(self, request):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        book_issue_counts = Book.objects.filter(bookissue__issued_at__gte=one_year_ago) \
            .annotate(issue_count=Count('bookissue')) \
            .order_by('-issue_count')
        serializer = BookIssueCountSerializer(book_issue_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def top_100_books_returned_late(self, request):
        top_100_books_late_returns = Book.objects.filter(bookissue__returned_at__gt=F('bookissue__have_to_return_at')). \
                                         annotate(
            late_return_count=Count('bookissue', bookissue__returned_at__gt=F(
                'bookissue__have_to_return_at'))) \
                                         .order_by('-late_return_count')[:100]

        serializer = TopLateReturnedBooksSerializer(top_100_books_late_returns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def top_100_clients_returned_books_late(self, request):
        top_100_users_late_returns = Client.objects.filter(
            bookissue__returned_at__gt=F('bookissue__have_to_return_at')). \
                                         annotate(late_return_count=Count('bookissue', bookissue__returned_at__gt=F(
            'bookissue__have_to_return_at'))) \
                                         .order_by('-late_return_count')[:100]

        serializer = TopLateReturnedUserSerilizer(top_100_users_late_returns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
