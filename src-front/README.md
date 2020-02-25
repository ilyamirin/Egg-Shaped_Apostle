# PlacesSearch


## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Docker development server

1. Run `make local.mk`
2. Run `yarn install`
3. Run `make server`
4. Go to `127.0.0.1:4200` in browser

## Docker production server

1. Run `make local.mk`
2. Change values in file `local.mk`
    * `ENV = prod`
    * `IMAGE_NAME` - image name
3. Run `make build`
4. Change `image` property in `docker-compose.prod.yaml` like `IMAGE_NAME` value
5. Run `make server`
6. Go to `<server ip>:80` in browser

## How to build without Docker

1. Run `yarn isntall`
2. Run `yarn run build`
3. Project files in `dist` folder
4. Configure Nginx (example in `docker/default.conf` file)
