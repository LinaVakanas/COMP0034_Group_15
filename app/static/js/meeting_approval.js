function changeResponse() {
    let isApproved = $('#isApproved input:radio:checked').val();
    let para = document.createElement("p");
    if (isApproved === "yes") {
        para.innerHTML = "Nice, we'll let ...";
        document.body.appendChild(para);
    } else {
        para.innerHTML = "Aw man. We'll let your mentor know you couldn't make it, and they'll hopefully book another " +
            "meeting which you can both make it to.";
        document.body.appendChild(para);
    }
}

