package com.example.abraacaixa;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class ConfigurarCodigo extends AppCompatActivity {
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference batida = database.getReference("chave").child("codigo_batidas");
    DatabaseReference numerico = database.getReference("chave").child("codigo_numerico");
    DatabaseReference rotacao = database.getReference("chave").child("codigo_rotacoes");

    String TAG = null;

    //Inputs do código
    EditText editBati;
    EditText editNum;
    EditText editRota;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.configurar_codigo);

        editBati = (EditText) findViewById(R.id.EditBatidas);
        editNum = (EditText) findViewById(R.id.EditNumerico);
        editRota = (EditText) findViewById(R.id.EditRotacoes);
    }

    public void GuardarCodigo (View v) {
        batida.setValue(editBati.getText().toString());
        numerico.setValue(editNum.getText().toString());
        rotacao.setValue(editRota.getText().toString());
        Toast.makeText(this, "Código configurado com sucesso ", Toast.LENGTH_SHORT).show();
        cancel(v);
    }

    public void cancel (View v) {
        Intent i = new Intent(this, MainActivity.class);
        startActivity(i);
    }

    public void onDataChange(DataSnapshot dataSnapshot) {
        // This method is called once with the initial value and again
        // whenever data at this location is updated.
        String value = dataSnapshot.getValue(String.class);
        Log.d(TAG, "Value is: " + value);
    }

    public void onCancelled(DatabaseError error) {
        // Failed to read value
        Log.w(TAG, "Failed to read value.", error.toException());
    }
}
