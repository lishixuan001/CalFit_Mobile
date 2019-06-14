package online.calfit.calfit_android;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.support.v4.app.NotificationCompat;

/**
 * Created by lishixuan001 on 6/1/19.
 */

public class NotificationReciever extends BroadcastReceiver {

    String contentText;
    @Override
    public void onReceive(Context context, Intent intent) {
        String intentAction = intent.getAction();
        if (intentAction.equals("notify_morning")) {
            contentText = "Your goal for today is ready!";
        } else {
            contentText = "Remember to upload your data!";
        }
        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        Intent intent1 = new Intent(context,MainActivity.class);
        intent1.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        // if we want ring on notifcation then uncomment below line//
        Uri alarmSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        PendingIntent pendingIntent = PendingIntent.getActivity(context,100,intent1,PendingIntent.FLAG_UPDATE_CURRENT);
        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, intentAction).
                setSmallIcon(R.drawable.logo).
                setContentIntent(pendingIntent).
                setContentText(contentText).
                setContentTitle("Calfit Reminder").
                setSound(alarmSound).
        setAutoCancel(true);
        notificationManager.notify(100, builder.build());
    }
}
