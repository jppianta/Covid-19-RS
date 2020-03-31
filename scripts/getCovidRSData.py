import requests
import json


class Covid19RS:
    def __init__(self):
        self.atualizarDados()

    def receberDadosDaVariavel(self, nomeVar, idx=0):
        return list(
            filter(lambda line: line.startswith(nomeVar), self.dados))[idx]

    def atualizarDados(self):
        url = "http://ti.saude.rs.gov.br/covid19/"

        # sending get request and saving the response as response object
        r = requests.get(url=url)

        infoPagina = r.text

        self.dados = infoPagina.split('\n')

    def casosPorCidade(self):
        graficoEstados = self.receberDadosDaVariavel('var myChart')

        graficoEstados = graficoEstados.split('data: ')

        estadosText = graficoEstados[1]

        estadosStart = estadosText.index('[')
        estadosEnd = estadosText.index(']')

        estados = estadosText[estadosStart+1:estadosEnd].split(',')

        estados = list(
            map(lambda estado: estado.replace('"', '').strip(), estados))

        casosText = graficoEstados[2]

        casosStart = casosText.index('[')
        casosEnd = casosText.index(']')

        casos = list(map(lambda val: int(val),
                         casosText[casosStart+1:casosEnd].split(',')))

        mapaDeCasos = dict()

        for idx in range(0, len(estados)):
            mapaDeCasos[estados[idx]] = casos[idx]

        return mapaDeCasos

    def casosPorGenero(self):
        graficoGenero = self.receberDadosDaVariavel('var ctxP')

        graficoGenero = graficoGenero.split('datasets: [{')[1]

        dadosStart = graficoGenero.index('[')
        dadosEnd = graficoGenero.index(']')

        dados = json.loads(graficoGenero[dadosStart:dadosEnd+1])

        return {'masculino': dados[0], 'feminino': dados[1]}

    def casosPorFaixaEtaria(self):
        graficoFaixaEtaria = self.receberDadosDaVariavel('var ctx ', 2)

        graficoFaixaEtaria = graficoFaixaEtaria.split('datasets: [{')

        labels = graficoFaixaEtaria[0]

        labelsStart = labels.index('[')
        labelsEnd = labels.index(']')

        labels = json.loads(labels[labelsStart:labelsEnd+1])

        dados = graficoFaixaEtaria[1]

        dadosStart = dados.index('[')
        dadosEnd = dados.index(']')

        dados = json.loads(dados[dadosStart:dadosEnd+1])

        mapaFaixaEtaria = dict()

        for idx in range(0, len(labels)):
            mapaFaixaEtaria[labels[idx]] = dados[idx]

        return mapaFaixaEtaria

    def casosPorDia(self):
        graficoDados = self.receberDadosDaVariavel('var myBarChar')

        graficoDados = graficoDados.split('datasets: [{')

        labels = graficoDados[0]

        labelsStart = labels.index('[')
        labelsEnd = labels.index(']')

        labels = json.loads(labels[labelsStart:labelsEnd+1])

        dados = graficoDados[1]

        dadosStart = dados.index('[')
        dadosEnd = dados.index(']')

        dados = json.loads(dados[dadosStart:dadosEnd+1])

        mapaCasosPorDia = dict()

        for idx in range(0, len(labels)):
            mapaCasosPorDia[labels[idx]] = dados[idx]

        return mapaCasosPorDia

    def receberDados(self):
        return {
            'dia': self.casosPorDia(),
            'cidade': self.casosPorCidade(),
            'faixaEtaria': self.casosPorFaixaEtaria(),
            'genero': self.casosPorGenero()
        }

    def exportarDados(self, nomeArquivoSaida):
        f = open(nomeArquivoSaida, "w")

        dados = self.receberDados()

        dadosJson = json.dumps(dados)
        f.write(dadosJson)
        f.close()


covidRS = Covid19RS()

covidRS.exportarDados('dadosRS.json')