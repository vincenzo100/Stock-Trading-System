const x = document.getElementById("view");
const y = document.getElementById("viewText");

x.addEventListener("mouseover", viewYes);
x.addEventListener("mouseleave", viewNo);

function viewYes() {
    y.style.visibility ="visible";
}

function viewNo() {
    y.style.visibility ="hidden";
}

const c = document.getElementById("buy");
const k = document.getElementById("buyText");

c.addEventListener("mouseover", buyYes);
c.addEventListener("mouseleave", buyNo);

function buyYes() {
    k.style.visibility ="visible";
}

function buyNo() {
    k.style.visibility ="hidden";
}

const m = document.getElementById("transfer");
const p = document.getElementById("transferText");

m.addEventListener("mouseover", transferYes);
m.addEventListener("mouseleave", transferNo);

function transferYes() {
    p.style.visibility ="visible";
}

function transferNo() {
    p.style.visibility ="hidden";
}
