from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.manage, name='Manage'),
    path('add-book/', views.addbook_view, name='AddBook'),
    path('view-books/', views.viewbooks_view, name='ViewBooks'),
    path('edit-book/<int:pk>/', views.editbook_view, name='EditBook'),
    path('delete-book/<int:pk>/', views.deletebook_view, name='DeleteBook'),
    path('delete-issued-book/<int:pk>/', views.delete_issued_book_view, name='DeleteIssuedBook'),
    path('issue-book/<int:pk>/', views.issuebook_view, name='IssueBook'),
    path('issued-book/', views.issuedbook_view, name='IssuedBooks'),
    path('issued-book-by-student/', views.issuedbookbystudent_view, name='IssuedBooksByStudent'),
    path('generate-reports/', views.generatereports_view, name='GenerateReportsView'),
    path('generate-report/', views.generate_report_view, name='GenerateReport'),
    path('generate-all-books-report/', views.render_all_books_report_view, name='GenerateAllBooksReportView'),
    path('generate-all-available-books-report/', views.render_all_available_books_report_view, name='GenerateAllAvailableBooksReportView'),
    path('generate-all-issued-books-report/', views.render_all_issued_books_report_view, name='GenerateAllIssuedBooksReportView'),
    path('generate-all-not-available-books-report/', views.render_all_not_available_books_report_view, name='GenerateAllNotAvailableBooksReportView'),
]
