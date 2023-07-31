echo "Installing poetry..."
curl -sSL https://install.python-poetry.org | python3 - || exit
echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc
poetry config virtualenvs.in-project true

echo "Installing dependencies..."
cd /workspaces/wilem
poetry install || exit
echo "Done!"

echo "Migrating models"
echo "Done"
