# ApisLM Expert Productivity Makefile

.PHONY: help install dev-backend dev-frontend dev-mobile dev-desktop test build-desktop docker-up docker-down clean

help: ## Show this help menu
	@echo "ApisLM Expert Productivity Commands:"
	@echo "------------------------------------"
	@findstr /R /C:"^[a-zA-Z0-9_-]*:.*##" $(MAKEFILE_LIST)

install: ## Install all dependencies across the monorepo
	@echo "Installing Backend dependencies..."
	cd ApisLM_Local_Backend && pip install -r requirements.txt || echo "Use virtualenv"
	@echo "Installing Workspace/Frontend dependencies..."
	cd ApisLM_Workspace/cloud-tenant-dashboard && npm install
	@echo "Installing Mobile dependencies..."
	cd ApisLM_Mobile_Edge && npm install
	@echo "Installing Desktop App dependencies..."
	cd ApisLM_Desktop_App && npm install

dev-backend: ## Run the local FastAPI server with hot-reload
	cd ApisLM_Local_Backend && uvicorn main_api:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run the Next.js cloud dashboard
	cd ApisLM_Workspace/cloud-tenant-dashboard && npm run dev

dev-mobile: ## Start Expo for the React Native Edge App
	cd ApisLM_Mobile_Edge && npx expo start

dev-desktop: ## Boot the Electron wrapper
	cd ApisLM_Desktop_App && npm start

test: ## Run the Queen Bee regression suite and all unit tests
	cd ApisLM_Self_Evolution && pytest queen_bee.py -v
	cd ApisLM_Local_Backend && pytest -v

build-desktop: ## Compile standalone .exe and .dmg desktop installers
	cd ApisLM_Desktop_App && npm run dist

docker-up: ## Spin up the entire ecosystem in Docker containers
	docker-compose up --build -d

docker-down: ## Tear down the Docker containers
	docker-compose down

clean: ## Remove node_modules, build artifacts, and Python cache
	@echo "Cleaning up..."
	FOR /D /R %%X IN (node_modules) DO RMDIR /S /Q "%%X"
	FOR /D /R %%X IN (__pycache__) DO RMDIR /S /Q "%%X"
