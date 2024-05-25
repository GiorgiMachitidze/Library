from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, viewsets
from rest_framework.decorators import action

from .permissions import IsEmployer, IsClient
from rest_framework import status
from rest_framework.response import Response
from .serializers import *


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

    @action(detail=True, methods=['post', 'get'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        if book.reserved_quantity == 0:
            return Response({'status': 'Book is not reserved'}, status=400)
        book.reserved_quantity -= 1
        book.stock_quantity += 1
        book.save()
        book_issue = BookIssue.objects.filter(book=book, returned_at__isnull=True).first()
        if book_issue:
            book_issue.returned_at = datetime.now() - \
                                     timedelta(hours=4)
            book_issue.save()
        else:
            return Response({'status': 'No book issue found'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'status': 'Book returned',
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
            BookIssue.objects.create(book=book, client=client, issued_at=reservation.reserved_at)
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
