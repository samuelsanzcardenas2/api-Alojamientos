from app import create_app

# Creamos la aplicacion
app = create_app()

if __name__ == "__main__":
    # Modo debug para reinicio automatico al guardar cambios
    app.run(debug=True, port=5000)
