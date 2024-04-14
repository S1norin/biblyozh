const btns = document.querySelectorAll("[data-target]");
const close_modals = document.querySelectorAll(".close-modal");
const overlay = document.getElementById("overlay");

btns.forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelector(btn.dataset.target).classList.add("active");
    overlay.classList.add("active");
  });
});

close_modals.forEach((btn) => {
  btn.addEventListener("click", () => {
    const modal = btn.closest(".modal");
    modal.classList.remove("active");
    overlay.classList.remove("active");
  });
});

window.onclick = (event) => {
  if (event.target == overlay) {
    const modals = document.querySelectorAll(".modal");
    modals.forEach((modal) => modal.classList.remove("active"));
    overlay.classList.remove("active");
  }
};

$(document).ready(function () {
    $("#btn").click(
        function () {
            const element = document.getElementById('bookmark');

            if (element.style.display === 'none') {
                element.style.display = 'inherit';
            } else {
                element.style.display = 'none';
            }

            const element2 = document.getElementById('bookmark-filled');

            if (element2.style.display === 'none') {
                element2.style.display = 'inherit';
            } else {
                element2.style.display = 'none';
            }
            const data = {
                book_id: $("#book_id").val(),
                page: $("#page").val(),
            };
            sendAjaxForm('bookmark_form', 'make_bookmark', data);
            return false;
        }
    );
});

function sendAjaxForm(ajax_form, url, data) {
    $.ajax({
        url: url,
        type: "POST",
        dataType: "html",
        data: data,
        success: function (response) {
            console.log("Отправлено");
        },
        error: function (response) {
            console.log("Ошибка");
        }
    });
}

function getSelectedTextIndices() {
    let startIndex, endIndex;
    const selection = window.getSelection();

    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const selectedText = range.toString();
        const allText = document.getElementById('content').textContent;
        console.log('here');
        startIndex = allText.indexOf(selectedText);
        endIndex = startIndex + selectedText.length;
    }
    console.log({start: startIndex, end: endIndex})
    const data = {start: startIndex, end: endIndex, page: document.getElementById('page').value};
    sendAjaxForm('highlight_form', 'highlight', data)
}
