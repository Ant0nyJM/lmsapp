from django.forms import ModelForm
from lmsapp.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_name','book_author','book_edition','book_genre']