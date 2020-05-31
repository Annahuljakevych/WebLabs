
class ExchangeTracker {

    constructor(baseURL, symbols, staticFilters, dynamicFilters, token) {
        this.baseURL = baseURL;
        this.symbols = symbols;
        this.static = staticFilters;
        this.dynamic = dynamicFilters;
        this.token = token;

        this.time = Date.now();
    }

    getUrl(isStatic = false) {
        const smb = this.getQuery(this.symbols, "symbols");
        const flt = this.getFilters(isStatic);

        return `${this.baseURL}?${smb}&${flt}&types=quote&token=${this.token}`
    }


    getQuery(args, name) {
        let query = name + "=";

        for (const arg of args) {
            query += arg + ',';
        }

        return query.substring(0, query.length - 1);
    }

    getFilters(isStatic) {
        if (isStatic) {
            return this.getQuery(this.static.concat(this.dynamic), "filter")
        }
        return this.getQuery(this.dynamic, "filter")
    }


    async getData(fetchUrl) {
        let data = await this.fetchData(fetchUrl);
        return this.parseData(data);
    }


    parseData(data) {
        let dataArray = [];

        for (var key in data) {
            let quote = data[key]["quote"];
            quote.previousClose = (quote.previousClose - quote.latestPrice).toFixed(2)
            dataArray.push(quote);
        }

        return dataArray;
    }

    async fetchData(url) {
        let response = await fetch(url);

        if (!response.ok) {
            console.log("Error HTTP code: " + response.status);
            return "";
        }

        return response.json();
    }


    updateTable(data) {
        let tableData = [];
        const keys = Object.keys(data[0])
        for (const key of keys) {
            tableData.push(document.getElementsByClassName(key));
        }


        for (let i = 0; i < data.length; i++) {
            let values = Object.values(data[i])
            for (let j = 0; j < values.length; j++) {
                tableData[j][i].innerHTML = values[j];
            }
        }

        this.time = Date.now();
    }

    updateTimeWorker() {
        let timeDiff = (Date.now() - this.time) / 1000
        document.getElementById('time').textContent = timeDiff.toFixed(1);
    }


    async updateTableWorker(partialUrl) {
        let data = await this.getData(partialUrl);
        this.updateTable(data);
    }

    async createTable(fullUrl, columnNames) {
        let data = await this.getData(fullUrl);
        this.buildTable(data, columnNames);
    }

    buildTable(rows, columnNames) {
        let html = '<table id="data-table">';
        html += '<tr>';

        for (let j of columnNames) {
            html += '<th>' + j + '</th>';
        }

        html += '</tr>';
        for (let i = 0; i < rows.length; i++) {
            html += '<tr>';
            for (let j in rows[i]) {
                html += `<td class="${j}">` + rows[i][j] + '</td>';
            }
            html += '</tr>';
        }
        html += '</table>';

        document.getElementById('container').innerHTML = html;
    }

    run() {
        const fullURL = this.getUrl(true);
        const partialURL = this.getUrl();

        let columnNames = ["Company name", "Position name", "Latest priñe", "Latest priñe diff"];
        this.createTable(fullURL, columnNames)
        rxjs.interval(100)
            .subscribe(() => {
                this.updateTimeWorker();
            });

        rxjs.interval(20000)
            .subscribe(() => {
                this.updateTableWorker(partialURL);
            });
    }
}

companies = [
    "AAPL",
    "FB",
    "TSLA",
    "AMZN",
    "MSFT",
    "KO",
    "SPOT",
    "NFLX",
    "NOK",
    "SNE"
]

staticFilters = ["symbol", "companyName"]
dynamicFilters = ["latestPrice", "previousClose"]

new ExchangeTracker("https://cloud.iexapis.com/v1/stock/market/batch",
    companies,
    staticFilters,
    dynamicFilters,
    "token-placeholder").run();