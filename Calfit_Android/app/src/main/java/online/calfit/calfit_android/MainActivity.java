package online.calfit.calfit_android;

import android.app.Activity;
import android.app.AlarmManager;
import android.app.AlertDialog;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.NotificationManagerCompat;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;

public class MainActivity extends Activity {

    private WebView myWebView;
    private static final String TAG = "MainActivity";

    DatabaseHelper mDatabaseHelper;
    private Button btnSubmit;
    private EditText editText1, editText2;
    private LinearLayout linearLayout;
    public final String CHANNEL_ID = "001";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

        /* Fetch Linear Layout */
        linearLayout = findViewById(R.id.linearLayout);

        /* Check Database See If Already Stores Data */
        ArrayList<String> listData = collectData();
        if (listData.size() > 0) {
            linearLayout.setVisibility(View.GONE);
            String actigraphId = listData.get(0);
            openWebView(actigraphId);
        } else {
            /* Collect User Input From The Front Page Text Box */
            editText1 = findViewById(R.id.Actigraph1);
            editText2 = findViewById(R.id.Actigraph2);
            btnSubmit = findViewById(R.id.btnSubmit);
            mDatabaseHelper = new DatabaseHelper(this);

            /* Respond to Submit Button */
            btnSubmit.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    /* Check If Two Text Boxes Have Same Input */
                    String actigraphID1 = editText1.getText().toString();
                    String actigraphID2 = editText2.getText().toString();
                    if (actigraphID1.equals(actigraphID2)) {
                        AddData(actigraphID1);
                        linearLayout.setVisibility(View.GONE);
                        set_notifications("notify_morning");
                        set_notifications("notify_evening");
                        openWebView(actigraphID1);
                    } else {
                        editText1.setText("");
                        editText2.setText("");
                        toastMessage("Please confirm your ActigraphID!");
                    }

                }
            });
        }
    }


    /** Set Up Notification
     * :param actionType -> "notify_morning" or "notify_evening" */
    public void set_notifications(String actionType) {
        int hour, minute;

        if (actionType.equals("notify_morning")) {
            hour = 8;
            minute = 0;
        } else {
            hour = 20;
            minute = 0;
        }

        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.HOUR_OF_DAY, hour);
        calendar.set(Calendar.MINUTE, minute);

        Intent intent = new Intent(getApplicationContext(), NotificationReciever.class);
        intent.setAction(actionType);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(getApplicationContext(), 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);

        AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
        assert alarmManager != null;
        alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), AlarmManager.INTERVAL_DAY, pendingIntent);
        Log.d(TAG, "Notification Initialized: [" + actionType + "]");

    }

    /** Get Android API Version */
    public int getAndroidVersion() {
        String release = Build.VERSION.RELEASE;
        int sdkVersion = Build.VERSION.SDK_INT;
        return sdkVersion;
    }

    /** Open the WebView Page */
    public void openWebView(String actigraphId) {
        // Define WebView
        myWebView = findViewById(R.id.webView);
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        // Load WebView - Check Internet Connection
        if (haveNetwork()) {
            myWebView.loadUrl("https://modesto.ieor.berkeley.edu/calfit/index/" + actigraphId);
            myWebView.setWebViewClient(new WebViewClient());
        } else {
            showInternetAlertDialog();
        }
    }

    /** Add Data To Database -> used when first usage of the App, user input their Actigraph ID*/
    public void AddData(String newEntry) {
        boolean insertData = mDatabaseHelper.addData(newEntry);

        if (insertData) {
            toastMessage("Data Successfully Inserted!");
        } else {
            toastMessage("Something went wrong");
        }
    }

    /** Collect Data From Database */
    public ArrayList<String> collectData() {
        //get the data and append to a list
        mDatabaseHelper = new DatabaseHelper(this);
        Cursor data = mDatabaseHelper.getData();
        ArrayList<String> listData = new ArrayList<>();
        while(data.moveToNext()){
            //get the value from the database in column 1
            //then add it to the ArrayList
            listData.add(data.getString(1));
        }
        return listData;
    }

    /**
     * customizable toast
     * @param message
     */
    private void toastMessage(String message){
        Toast.makeText(this,message, Toast.LENGTH_SHORT).show();
    }

    /** Check If Has Network Or Not */
    private boolean haveNetwork() {
        boolean have_WIFI=false;
        boolean have_MobileData=false;

        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
        NetworkInfo[] networkInfos = connectivityManager.getAllNetworkInfo();

        for(NetworkInfo info:networkInfos){
            if(info.getTypeName().equalsIgnoreCase("WIFI"))
                if(info.isConnected())
                    have_WIFI=true;
            if(info.getTypeName().equalsIgnoreCase("MOBILE"))
                if(info.isConnected())
                    have_MobileData=true;
        }
        return have_MobileData || have_WIFI;
    }

    /** Show Alert If No Internet */
    public void showInternetAlertDialog() {

        AlertDialog.Builder alert = new AlertDialog.Builder(this);
        alert.setTitle("No Internet");
        alert.setIcon(android.R.drawable.ic_dialog_alert);
        alert.setMessage("Network not available!");
        alert.setNeutralButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                toastMessage("Please Check your Network");
                dialogInterface.cancel();
            }
        });
        alert.create().show();
    }

    public void showInternetAlert() {
        AlertDialog alertDialog = new AlertDialog.Builder(this)
                //set icon
                .setIcon(android.R.drawable.ic_dialog_alert)
                //set title
                .setTitle("No Internet")
                //set message
                .setMessage("Network not available!")
                //set positive button
                .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        //set what would happen when positive button is clicked
                        toastMessage("Please Check your Network");
                    }
                })
                //set negative button
                .setNegativeButton("No", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        //set what should happen when negative button is clicked
                        toastMessage("Please Check your Network");
                    }
                })
                .show();
    }

    @Override
    public void onBackPressed() {
        if (myWebView.canGoBack()) {
            /* TODO -> Can Go Back When Click "Back"? */
            myWebView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
