package com.example.abraacaixa;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import android.app.PendingIntent;

import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.ContactsContract;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.widget.Button;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.content.Intent;
import android.widget.Toast;
import android.app.NotificationManager;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {

    String TAG = null;
    FirebaseDatabase database;
    DatabaseReference mReferenceEstado;
    DatabaseReference mReferenceSom;
    DatabaseReference mReferenceInput;


    String estadoBD;
    String somBD;
    String estadoInputBD;

    TextView estado;
    TextView ckRotacao;
    TextView ckNumerico;
    TextView ckBatida;

    Button changeEstado;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        database = FirebaseDatabase.getInstance();
        mReferenceEstado = database.getReference("estado");
        mReferenceSom = database.getReference("som");
        mReferenceInput = database.getReference("codigo").child("partes_corretas");


        estado = (TextView) findViewById(R.id.TextEstado);
        changeEstado = (Button) findViewById(R.id.AbrirCaixa);
        ckRotacao = (TextView) findViewById(R.id.CheckRotacoes);
        ckNumerico = (TextView) findViewById(R.id.CheckNumerico);
        ckBatida = (TextView) findViewById(R.id.CheckBatidas);

        //Listener para verificar alterações no estado da caixa
        mReferenceEstado.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.exists()) {
                    estadoBD = snapshot.getValue().toString();
                    estado.setText(estadoBD);
                    //noficacoes();
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {

            }
        });

        //Listener para verificar alterações na variável som
        mReferenceSom.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.exists()) {
                    somBD = snapshot.getValue().toString();
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {

            }
        });

        //Listener para verificar alterações no estado da Input dos elementos do código
        mReferenceInput.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.exists()) {
                    estadoInputBD = snapshot.getValue().toString();
                    checkInput();
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {

            }
        });

        }

    public void configCodigo (View v) {
        Intent i = new Intent(this, ConfigurarCodigo.class);
        startActivity(i);
    }

    public void alterarEstado (View v){
        if (estadoBD.equals("Aberto")){

      new AlertDialog.Builder(this)
              .setTitle("Fechar a Caixa")
              .setMessage("Tem a certeza que pretende fechar a caixa?")
              .setIcon(android.R.drawable.ic_dialog_alert)
              .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                  @Override
                  public void onClick(DialogInterface dialog, int which) {
                      mReferenceEstado.setValue("Fechado");
                      Toast.makeText(MainActivity.this, "Caixa fechado com sucesso!",  Toast.LENGTH_LONG).show();

                  }
              })
              .setNegativeButton(android.R.string.no, null).show();
        } else {
            new AlertDialog.Builder(this)
                    .setTitle("Abrir a Caixa")
                    .setMessage("Tem a certeza que pretende abrir a caixa?")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            mReferenceEstado.setValue("Aberto");
                            Toast.makeText(MainActivity.this, "Caixa aberta com sucesso!",  Toast.LENGTH_LONG).show();

                        }
                    })
                    .setNegativeButton(android.R.string.no, null).show();
        }
    }

    public void checkInput () {
        if(estadoInputBD.equals("3")) {
            ckRotacao.setText("Correto");
        }

        if(estadoInputBD.equals("32")) {
            ckRotacao.setText("Correto");
            ckNumerico.setText("Correto");
        }
        if (estadoInputBD.equals("321")){
            ckRotacao.setText("Correto");
            ckNumerico.setText("Correto");
            ckBatida.setText("Correto");
        }
        if (estadoInputBD.isEmpty()){
            ckRotacao.setText("");
            ckNumerico.setText("");
            ckBatida.setText("");
        }
    }


    public void desativarAlarme (View v) {
        if (somBD.equals("True")) {
            new AlertDialog.Builder(this)
                    .setTitle("Desativar alarme")
                    .setMessage("Tem a certeza que pretende desativar o alarme?")
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Toast.makeText(MainActivity.this, "Alarme sonoro desativado",  Toast.LENGTH_LONG).show();
                            mReferenceSom.setValue("False");
                        }
                    })
                    .setNegativeButton(android.R.string.no, null).show();
        } else {
            Toast.makeText(MainActivity.this, "Não existe sinal sonoro ativo!",  Toast.LENGTH_LONG).show();
        }
    }

    public void noficacoes (View v){
        NotificationCompat.Builder builder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.drawable.common_google_signin_btn_icon_dark)
                .setContentTitle("My notification")
                .setContentText("Much longer text that cannot fit one line...")
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText("Much longer text that cannot fit one line..."))
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

        Intent ni = new Intent(this, MainActivity.class);
        PendingIntent contentIntent = PendingIntent.getActivity(this, 0, ni, PendingIntent.FLAG_UPDATE_CURRENT);
        builder.setContentIntent(contentIntent);

        NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        manager.notify(0, builder.build());

    }


    public void onCancelled(DatabaseError error) {
        // Failed to read value
        Log.w(TAG, "Failed to read value.", error.toException());
    }



}

