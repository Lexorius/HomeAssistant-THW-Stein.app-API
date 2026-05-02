# Changelog

## [0.6.2]
* CI: hassfest-, HACS- und Python-Checks-Workflow ergänzt; Release-Workflow baut `thw_stein.zip` aus Tags `v*`.
* `manifest.json`: Key-Reihenfolge an HA-Konvention angepasst (domain, name, dann alphabetisch).
* `hacs.json`: nicht-schemakonforme Keys (`domains`, `logo`) entfernt.
* Lint-Cleanup: ungenutzte `datetime.datetime`/`datetime.timezone`-Imports entfernt, Imports sortiert, fehlende Trailing-Newlines ergänzt.
* CHANGELOG auf `## [VERSION]`-Format umgestellt (Voraussetzung für Release-Notes-Extraktion).

## [0.6.1]
* `spValidUntil` (Sicherheitsprüfung) analog zu `huValidUntil` hinzugefügt.
  Neue Attribute: `spValidUntil`, `sp_remaining_hours`, `sp_status`.
* HU-Restlaufzeit-Helper zu generischer Funktion refactored (wird für HU und SP genutzt).

## [0.4.0]
* unter Einsatzvorbehalt - eingefügt.

## [0.3.7]
* def _handle_coordinator_update(self)  aktualisiert

## [0.3.6]
* changelog korrigiert.
* Sensor naming reworked

## [0.3.4]
* my stupidity with the manifest.json....

## [0.3.1b]
* set default time to sync to 60 sec
* deleted the get_asset_detail - not needeed -

## [0.2.7]
* Added per‑asset sensors with status & attributes
* Updated README and manifest

## [0.2.6]
* Introduced DataUpdateCoordinator polling
* First working BU‑ID + Bearer auth implementation

## [0.2.5]
* Initial Bearer token setup, minimal client

## [0.2.1]
* Switched to Authorization header (Bearer)

## [0.2.0]
* Removed x-api-key, switched to API key only

## [0.1.0]
* Added documentation & cleanup

## [0.0.5] – [0.0.9]
* Early experimental versions (login, x-api-key, fixes)
