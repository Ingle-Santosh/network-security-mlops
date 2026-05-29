train:
	python main.py

api:
	uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

ui:
	streamlit run streamlit_app/app.py

full:
	start cmd /k "uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload"
	start cmd /k "streamlit run streamlit_app/app.py"