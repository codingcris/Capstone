export default class HomePage {
  constructor() {
    this._contentElement = document.createElement("div");
    this.content.id = "homeContent";
    this.createCompaniesTable();
  }

  get content() {
    return this._contentElement;
  }

  createCompaniesTable() {
    fetch("./companies")
      .then((response) => response.json())
      .then((companies) => {
        let companiesTable = document.createElement("table");
        companiesTable.innerHTML = `
                <thead>
                    <tr>
                        <th colspan="3">
                            <h2>Companies</h2>
                        </th>
                    </tr>
                    <tr>
                        <th>Ticker</th>
                        <th>Company Name</th>
                        <th>Closing Price</th>
                    <tr>
                </thead>
            `;

        for (let company of companies) {
          let row = document.createElement("tr");
          let ticker = document.createElement("td");
          let name = document.createElement("td");
          let price = document.createElement("td");

          ticker.textContent = `${company.ticker}`;
          let nameSpan = document.createElement("span");
          nameSpan.setAttribute("data-ticker", company.ticker);
          nameSpan.classList.add("company-name");
          nameSpan.textContent = company.name;

          nameSpan.addEventListener("click", function () {
            const ticker = this.getAttribute("data-ticker");

            const event = new CustomEvent("companySelected", {
              detail: ticker,
              bubbles: true,
            });
            nameSpan.dispatchEvent(event);
          });
          name.appendChild(nameSpan);

          price.textContent = `0.0`;

          row.appendChild(ticker);
          row.appendChild(name);
          row.appendChild(price);
          companiesTable.appendChild(row);
        }
        this.content.append(companiesTable);
      });
  }
}
