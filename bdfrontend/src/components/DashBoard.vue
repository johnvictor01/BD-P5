<template>
    <div class="dashboard">
      <h1>Sobre seus rendimentos</h1>
  
      <!-- Gráfico de Pizza -->
      <div class="chart-container">
        <div class="pie-chart" :style="getPieChartStyle"></div>
      </div>
  
      <!-- Legenda -->
      <div class="legend">
        <div class="legend-item" v-for="(obra, index) in obras" :key="index">
          <span :style="{ backgroundColor: getColorForIndex(index) }" class="legend-color"></span>
          {{ obra.nome }}: R$ {{ obra.valor }}
        </div>
      </div>
      <br>
      <br>
      <p>Acima estão suas obras e quanto elas valem em receita monetária do Real</p>
  
      
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Dados das obras (JSON de teste)
        obras: [
          { nome: "vangogh", valor: 5000 },
          { nome: "Obra 2", valor: 3000 },
          { nome: "Obra 3", valor: 2000 },
          { nome: "Obra 3", valor: 2000 },
          { nome: "Obra 3", valor: 2000 },
          { nome: "Obra 4", valor: 1000 }
        ]
      };
    },
    computed: {
      // Calculando o total das obras
      totalValor() {
        return this.obras.reduce((sum, obra) => sum + obra.valor, 0);
      },
      // Função para calcular as porcentagens e gerar o conic-gradient dinamicamente
      getPieChartStyle() {
        let startAngle = 0;
        const slices = this.obras.map((obra) => {
          const percentage = (obra.valor / this.totalValor) * 100;
          const endAngle = startAngle + percentage;
          const color = this.getColorForIndex(this.obras.indexOf(obra));
          const slice = `${color} ${startAngle}% ${endAngle}%`;
          startAngle = endAngle;
          return slice;
        });
        return {
          background: `conic-gradient(${slices.join(', ')})`
        };
      }
    },
    methods: {
      // Função auxiliar para definir as cores das fatias
      getColorForIndex(index) {
        const colors = ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0'];
        return colors[index % colors.length];
      }
    }
  };
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .dashboard {
    text-align: center;
    padding: 20px;
  }
  
  .chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  
  .pie-chart {
    width: 200px;
    box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.3);
    height: 200px;
    border-radius: 50%;
    position: relative;
  }
  
  .legend {
    max-width: 80rem;
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
  }
  
  .legend-color {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 10px;
    border-radius: 50%;
  }
  
  .bar-chart-container {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    margin-top: 40px;
  }
  
  .bar-chart {
    display: flex;
    align-items: flex-end;
    height: 200px;
    margin-right: 10px;
  }
  
  .bar {
    width: 40px;
    margin: 0 5px;
  }
  
  .bar-labels {
    display: flex;
  }
  
  .bar-label {
    width: 40px;
    margin: 0 5px;
    text-align: center;
  }
  </style>