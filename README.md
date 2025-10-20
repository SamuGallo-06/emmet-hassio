# Emmet

> "Aspetta un attimo, Doc. Mi stai dicendo che hai costruito un assistente vocale... per Home Assistant?"

**Emmett** è un assistente vocale self-hosted, scritto in Python, progettato per integrarsi direttamente con [Home Assistant](https://www.home-assistant.io/).

Utilizza la wake-word personalizzata **"Hey Doc!"** per attivarsi e rimane in ascolto dei tuoi comandi. È costruito per essere leggero, privato e tematico.

L'obiettivo di questo progetto è fornire un'alternativa flessibile ai servizi cloud (come Alexa o Google) usando un motore di wake-word offline e l'elaborazione dei comandi locali o tramite le API di Home Assistant.

## Caratteristiche Principali

* **Wake-Word Offline:** Utilizza [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) per il rilevamento della wake-word "Hey Doc!" in modo efficiente e interamente offline.
* **Integrazione HA:** Progettato per inviare comandi, attivare script o automazioni sulla tua istanza di Home Assistant.
* **Flessibile:** Scritto in Python, facile da modificare ed estendere.
* **Privato:** La tua voce non lascia la tua rete locale (eccetto per la trascrizione dei comandi, se si sceglie di usare un'API cloud come Google Speech-to-Text).

## Requisiti

* Python 3
* Un'istanza di Home Assistant
* Un microfono
* Una AccessKey Picovoice (gratuita per uso personale)

## Licenza

Il codice sorgente di **Emmett** è rilasciato sotto la [Licenza MIT](LICENSE).

Si prega di notare che questo progetto dipende da Picovoice Porcupine, che è governato dalla [Licenza Apache 2.0](https://github.com/Picovoice/porcupine/blob/master/LICENSE). I modelli wake-word personalizzati generati tramite la Picovoice Console Free Tier sono limitati all'uso personale e non commerciale.
