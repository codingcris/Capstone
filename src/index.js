import HomePage from "./homePage.js";
import ViewTicker from "./viewTicker.js";

class Controller {
  constructor() {
    this.header = this.createHeader();
    this.footer = this.createFooter();
    this.initializeDocument();

    this.homePage = new HomePage();
    this.viewTicker = new ViewTicker();

    this.render(this.homePage.content);
    document.body.addEventListener("companySelected", (event) => {
      const ticker = event.detail;
      this.viewTicker.setTicker(ticker);
      this.render(this.viewTicker.content);
    });
  }

  initializeDocument() {
    const BODY = document.querySelector("body");

    const CONTENT = document.createElement("div");
    CONTENT.id = "content";

    BODY.append(this.header, CONTENT, this.footer);
  }

  createHeader() {
    const HEADER = document.createElement("header");
    HEADER.innerHTML = `
    <h1>InverstorBoost Tech</h1>
    <h1><a href="/">Stock Prediction Dashboard</a></h1>
    <input type="text"/>
    `;

    return HEADER;
  }

  createFooter() {
    const FOOTER = document.createElement("footer");
    FOOTER.innerHTML = `
    <a id="about">About Us</a>
    <a id"ourModels" href="/our-models">Our Models</a>
    `;

    return FOOTER;
  }

  render(content) {
    this.clearContent();
    const CONTENT = document.getElementById("content");
    CONTENT.appendChild(content);
  }

  clearContent() {
    const CONTENT = document.getElementById("content");
    CONTENT.innerHTML = "";
  }

  get contentElement() {
    return document.getElementById("content");
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  const domController = new Controller();
});
