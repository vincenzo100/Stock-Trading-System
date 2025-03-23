const x = document.getElementById("stock");
const y = document.getElementById("viewStock");

x.addEventListener("mouseover", stockYes);
x.addEventListener("mouseleave", stockNo);

function stockYes() {
    y.style.visibility ="visible";
}

function stockNo() {
    y.style.visibility ="hidden";
}

const c = document.getElementById("market");
const k = document.getElementById("viewMarket");

c.addEventListener("mouseover", marketYes);
c.addEventListener("mouseleave", marketNo);

function marketYes() {
    k.style.visibility ="visible";
}

function marketNo() {
    k.style.visibility ="hidden";
}

const m = document.getElementById("sched");
const p = document.getElementById("viewSched");

m.addEventListener("mouseover", schedYes);
m.addEventListener("mouseleave", schedNo);

function schedYes() {
    p.style.visibility ="visible";
}

function schedNo() {
    p.style.visibility ="hidden";
}
