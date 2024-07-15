from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from books.models import Book
import random
from django.contrib.auth.views import LogoutView


def verify_users_credentials(request):
    # Get the username and password from the request parameters
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Check if both username and password are provided
        if not (username and password):
            return JsonResponse(
                {"error": "Both username and password are required"}, status=400
            )

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # User with the provided credentials exists
            # Retrieve the list of books
            all_books = Book.objects.all()

            # Pick 3 random books if available, otherwise pick all available books
            if all_books.count() >= 3:
                random_books = random.sample(list(all_books), 3)
            else:
                random_books = all_books

            # rendering to dashboard.html
            return render(
                request,
                "dashboard.html",
                {"user": user, "random_books": random_books, "all_books": all_books},
            )
        # I want it to redirect to login_success.html
        else:
            # User with the provided credentials does not exist
            message = "Invalid credentials. Please try again."
            return render(request, "status.html", {"message": message})

    else:
        # Only GET requests are allowed
        message = "Method not allowed."
        return render(request, "status.html", {"message": message}, status=405)


# list all user
def list_users(request):
    if request.method == "GET":
        # Retrieve all users from the User model
        users = User.objects.all()

        # Serialize user data
        user_data = []
        for user in users:
            user_data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    # Add more fields as needed
                }
            )

        # Return JSON response containing user data
        return JsonResponse({"users": user_data})

    else:
        # Only GET requests are allowed
        message = "Method not allowed."
        return render(request, "status.html", {"message": message}, status=405)


# sign up a user
@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes only)
def sign_up(request):
    if request.method == "POST":
        # Get the username and password from the request parameters
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if both username and password are provided
        if not (username and password):
            message = "Both username and password are required."
            return render(request, "status.html", {"message": message}, status=400)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            message = "User exist. Please forget Password or try again."
            return render(request, "status.html", {"message": message}, status=400)

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Optionally, you can perform additional actions here, such as sending a confirmation email

        # Return a success response
        message = "User created successfully."
        return render(request, "status.html", {"message": message})

    else:
        # Only POST requests are allowed
        message = "Method not allowed."
        return render(request, "status.html", {"message": message}, status=405)


# forgot_password
@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes only)
def forgot_password(request):
    if request.method == "POST":
        # Get the username and new password from the request parameters
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        # Check if both username and new password are provided
        if not (username and new_password):
            message = "Both username and new password are required."
            return render(request, "status.html", {"message": message}, status=400)

        # Check if the user with the provided username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            message = "User does not exist."
            return render(request, "status.html", {"message": message}, status=400)

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        # Optionally, you can perform additional actions here, such as sending a confirmation email

        # Return a success response
        message = "Password updated successfully."
        return render(request, "status.html", {"message": message})

    else:
        # Only POST requests are allowed
        message = "Method not allowed."
        return render(request, "status.html", {"message": message}, status=405)


# def for rendering read_book.html and send the uploaded txt from book model
def read_book(request):
    if request.method == "POST":
        # Get the name of the book from the request
        book_name = request.POST.get("book_name")

        # Query the Book model to find the book with the given name
        books = Book.objects.filter(title=book_name)

        if books.exists():
            # Select the first book with the given name
            book = books.first()

            # Check the book type
            if book.book_type == "book":
                # Get the text file associated with the book
                text_file = book.text_file

                if text_file:
                    # Read the content of the text file
                    text_content = text_file.read().decode("utf-8")

                    # Render the read_book.html template with the text content
                    return render(
                        request, "read_book.html", {"text_content": text_content}
                    )
                else:
                    # If no text file is associated with the book, return an error response
                    return JsonResponse(
                        {"error": "No text file associated with the book."}, status=400
                    )
            else:
                return JsonResponse(
                    {"error": "The selected book is not a text book."}, status=400
                )
        else:
            # If no book with the given name is found, return an error response
            return JsonResponse(
                {"error": f'No book with the name "{book_name}" found.'}, status=400
            )
    else:
        return render(request, "read_book.html")


def watch_video(request):
    if request.method == "POST":
        # Get the name of the book from the request
        book_name = request.POST.get("book_name")

        # Query the Book model to find the book with the given name
        books = Book.objects.filter(title=book_name)

        if books.exists():
            # Select the first book with the given name
            book = books.first()

            # Check the book type
            if book.book_type == "video":
                # Get the associated movie
                movie = book.movie
                if movie:
                    # Render the watch_video.html template with the movie
                    return render(request, "watch_movie.html", {"movie": movie})
                else:
                    return JsonResponse(
                        {"error": "No video associated with the book."}, status=400
                    )
            else:
                return JsonResponse(
                    {"error": "The selected book is not a video book."}, status=400
                )
        else:
            # If no book with the given name is found, return an error response
            return JsonResponse(
                {"error": f'No book with the name "{book_name}" found.'}, status=400
            )
    else:
        return render(request, "watch_video.html")


logout_view = LogoutView.as_view(
    template_name="logout.html",
    next_page="/books/login/",  # redirect to login page after logout
    extra_context={"message": "You have been logged out."},
)
