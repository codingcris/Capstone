import * as LightweightCharts from "lightweight-charts";

export default class ViewTicker {
  constructor() {
    this._contentElement = document.createElement("div");
    this._contentElement.id = "tickerContent";
  }

  get content() {
    return this._contentElement;
  }

  setTicker(ticker) {
    function setupCandleStickChart(data, chartDiv) {
      const chart = LightweightCharts.createChart(chartDiv, {
        width: 600,
        height: 300,
        layout: {
          backgroundColor: "#ffffff",
          textColor: "rgba(0, 0, 0, 0.9)",
        },
        grid: {
          vertLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
          horzLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
        timeScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
      });

      const candlestickSeries = chart.addCandlestickSeries();
      candlestickSeries.setData(data);
    }

    function setupVolumeChart(originalData, chartDiv) {
      const transformedData = originalData.map((entry) => ({
        time: entry.time,
        value: entry.volume,
      }));

      const chart = LightweightCharts.createChart(chartDiv, {
        width: 600,
        height: 300,
        layout: {
          backgroundColor: "#ffffff",
          textColor: "rgba(0, 0, 0, 0.9)",
        },
        grid: {
          vertLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
          horzLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
        timeScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
      });

      const volumeSeries = chart.addHistogramSeries({
        color: "#26a69a",
        lineWidth: 1,
        priceFormat: {
          type: "volume",
        },
        overlay: true,
        scaleMargins: {
          top: 0.8,
          bottom: 0,
        },
      });

      volumeSeries.setData(transformedData);
    }

    function setupMovingAveragesChart(data, chartDiv) {
      const chart = LightweightCharts.createChart(chartDiv, {
        width: 600,
        height: 300,
        layout: {
          backgroundColor: "#ffffff",
          textColor: "rgba(0, 0, 0, 0.9)",
        },
        grid: {
          vertLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
          horzLines: {
            color: "rgba(197, 203, 206, 0.5)",
          },
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
        timeScale: {
          borderColor: "rgba(197, 203, 206, 0.8)",
        },
        handleScroll: {
          vertTouchDrag: false,
          mouseWheel: false,
          horzTouchDrag: false,
          vertMouseDrag: false,
        },
        handleScale: {
          axisPressedMouseMove: false,
          mouseWheel: false,
          pinch: false,
        },
      });

      // Adding line series for closing prices
      const lineSeries = chart.addLineSeries();
      lineSeries.setData(
        data.slice(-200).map((item) => ({ time: item.time, value: item.close }))
      );

      // Calculate 50-day moving average
      const movingAverage50 = calculateMovingAverage(data, 50);

      // Adding line series for 50-day moving average
      const ma50Series = chart.addLineSeries({
        color: "red",
        lineWidth: 2,
      });
      ma50Series.setData(movingAverage50);

      // Calculate 200-day moving average
      const movingAverage200 = calculateMovingAverage(data, 200);

      // Adding line series for 200-day moving average
      const ma200Series = chart.addLineSeries({
        color: "green",
        lineWidth: 2,
      });
      ma200Series.setData(movingAverage200);

      const lastData50 = movingAverage50[movingAverage50.length - 1];
      const lastData200 = movingAverage200[movingAverage200.length - 1];

      ma50Series.setMarkers([
        {
          time: lastData50.time,
          position: "aboveBar",
          color: "red",
          shape: "arrowUp",
          text: "MA 50                   ",
        },
      ]);

      ma200Series.setMarkers([
        {
          time: lastData200.time,
          position: "aboveBar",
          color: "green",
          shape: "arrowUp",
          text: "MA 200                   ",
        },
      ]);
    }
    function calculateMovingAverage(data, days) {
      let result = [];
      const start = Math.max(data.length - 200, days);
      for (let i = start; i < data.length; i++) {
        const lastDays = data.slice(i - days, i);
        const avg = lastDays.reduce((acc, val) => acc + val.close, 0) / days;
        result.push({ time: data[i].time, value: avg });
      }
      return result;
    }

    this.content.innerHTML = "";
    this.ticker = ticker;
    console.log(this);
    fetch("/ticker/" + ticker)
      .then((response) => response.json())
      .then((data) => {
        let tickerHeading = document.createElement("h1");
        tickerHeading.textContent = ticker;
        this.content.appendChild(tickerHeading);

        let candlestickChart = document.createElement("div");
        candlestickChart.id = "chart1";
        this.content.appendChild(candlestickChart);
        setupCandleStickChart(data.history, candlestickChart);

        let volumeChart = document.createElement("div");
        volumeChart.id = "chart2";
        this.content.appendChild(volumeChart);
        setupVolumeChart(data.history, volumeChart);

        let movingAveragesChart = document.createElement("div");
        movingAveragesChart.id = "chart3";
        this.content.appendChild(movingAveragesChart);
        setupMovingAveragesChart(data.history, movingAveragesChart);

        let infoTable = document.createElement("table");
        infoTable.id = "stockInfo";
        console.log(typeof data.info);
        const curatedInfo = {
          // Company Information
          longName: data.info.longName,
          industry: data.info.industry,
          sector: data.info.sector,
          address1: data.info.address1,
          phone: data.info.phone,
          website: data.info.website,

          // Stock Data
          currentPrice: data.info.currentPrice,
          dayHigh: data.info.dayHigh,
          dayLow: data.info.dayLow,
          volume: data.info.volume,
          averageVolume: data.info.averageVolume,

          // Financial Ratios
          beta: data.info.beta,
          priceToSalesTrailing12Months: data.info.priceToSalesTrailing12Months,
          priceToBook: data.info.priceToBook,
          trailingPE: data.info.trailingPE,
          forwardPE: data.info.forwardPE,

          // Market Performance
          "52WeekChange": data.info["52WeekChange"],
          SandP52WeekChange: data.info.SandP52WeekChange,
          marketCap: data.info.marketCap,

          // Dividends & Returns
          dividendRate: data.info.dividendRate,
          dividendYield: data.info.dividendYield,
          payoutRatio: data.info.payoutRatio,

          // Target Prices
          targetHighPrice: data.info.targetHighPrice,
          targetLowPrice: data.info.targetLowPrice,
          targetMeanPrice: data.info.targetMeanPrice,

          // Analyst Opinions
          numberOfAnalystOpinions: data.info.numberOfAnalystOpinions,
          recommendationKey: data.info.recommendationKey,
        };

        Object.entries(curatedInfo).forEach(([key, val]) => {
          let tableRow = document.createElement("tr");
          tableRow.innerHTML = `
            <th>${key}</th>
            <td>${val}</td>
          `;

          infoTable.appendChild(tableRow);
        });
        this.content.appendChild(infoTable);

        let predictButton = document.createElement("button");
        predictButton.textContent = "Predict";
        predictButton.addEventListener("click", (event) => {
          window.location.href = `/ticker/${this.ticker}/predict`;
        });
        this.content.appendChild(predictButton);
      });
  }
}
