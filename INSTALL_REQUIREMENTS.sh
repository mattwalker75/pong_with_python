
echo $VIRTUAL_ENV | grep pong_venv > /dev/null
if (( $? == 0 ))
then
   echo "We are in the correct environment..."
   echo "Installing packages:"
   pip install -r requirements.txt
else
   echo "In the wrong environment."
   echo "Run:  source pong_venv/bin/activate"
fi

