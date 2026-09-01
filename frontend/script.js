async function submitReview(productId) {

    const textarea = document.getElementById(
        "review" + productId
    );

    const review = textarea.value.trim();


    // Empty review check

    if (!review) {

        alert("Please enter your review");

        return;
    }


    try {

        // Python FastAPI ko review bhejna

        const response = await fetch(
            "http://127.0.0.1:8000/check-review",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    review: review
                })
            }
        );


        const data = await response.json();


        // Agar review positive hai

        if (data.show === true) {

            const reviewsContainer =
                document.getElementById(
                    "reviews" + productId
                );


            const reviewDiv =
                document.createElement("div");


            reviewDiv.classList.add(
                "review"
            );


            reviewDiv.innerText =
                data.review;


            reviewsContainer.appendChild(
                reviewDiv
            );


            // Textarea empty

            textarea.value = "";


            alert(
                "Positive review added!"
            );

        }


        // Agar negative hai

        else {

            textarea.value = "";

            alert(
                "Thankyou for your valuable feedback,we will enhance the product"
            );

        }

    }


    catch (error) {

        console.error(error);

        alert(
            "Server connection error. Make sure Python backend is running."
        );

    }

}