## 0.1.8
* Added debug logging for login parameters and JS fetch status

## 0.1.7
* Korrektur: content_in_root in hacs.json jetzt auf `false`
* Bugfix: korrekte Manifest-Version für HACS

## 0.1.5
* HACS-Fix: content_in_root auf `true` gesetzt

## 0.1.4
* Rewrote `config_flow.py` with valid indentation and clean OptionsFlow implementation

## 0.1.2
* Fix für `IndentationError` in `config_flow.py`

## 0.1.1
* Added multi-pattern API-key extraction
* OptionsFlow deprecation fix

# Changelog

## 0.1.0
* Dokumentation und Code-Kommentare vollständig ergänzt
* UI-Optionen integriert (ConfigFlow, OptionsFlow)
* Code vollständig asynchronisiert (aiohttp statt httpx)
* Bugfix: `X-API-KEY` Extraction robuster gemacht

## 0.0.8
* Fehlende Konstanten ergänzt
* `sensor.py` und `config_flow.py` wieder hinzugefügt

## 0.0.7
* Regex für `X-API-KEY` korrigiert (PatternError behoben)

## 0.0.6
* Fehlerhafte API-Initialisierung korrigiert

## 0.0.5
* Initialer Release mit Basis-Funktionalität
