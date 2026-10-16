# Database Backup and Restore

The production PostgreSQL database is hosted by Amazon RDS. Database passwords
must stay in AWS environment settings and must never be written in this file.

## Backup policy

- Enable RDS automated backups with a seven-day retention period.
- Create a manual snapshot before a risky migration or destructive database
  change.
- Create a final snapshot before deleting the production database.
- Keep the current database until a restored database has been tested.

## Confirm automated backups

1. Open the Amazon RDS console in the same AWS Region as the application.
2. Choose **Databases**, then choose the production database instance.
3. Open **Maintenance & backups**.
4. Confirm that automated backups are enabled and the retention period is seven
   days.
5. If the setting is changed, wait until the database returns to the
   **Available** state.

## Create a manual snapshot

1. In the RDS console, choose **Databases** and select the production database.
2. Choose **Actions**, then **Take snapshot**.
3. Give the snapshot a descriptive name containing the date and reason, such as
   `workout-tracker-before-migration-YYYY-MM-DD`.
4. Create the snapshot and wait until its status is **Available** before making
   the risky change.

## Restore from a snapshot

Restoring a snapshot creates a new RDS database instance. It does not overwrite
the original instance.

1. In the RDS console, choose **Snapshots**.
2. Select the required snapshot, choose **Actions**, then **Restore snapshot**.
3. Give the restored instance a new, unique identifier.
4. Place it in the same VPC and security group configuration used by the
   application.
5. Wait until the restored instance is **Available**, then copy its endpoint.
6. In the Elastic Beanstalk environment settings, update `POSTGRES_HOST` to the
   restored endpoint. Confirm that `POSTGRES_PORT`, `POSTGRES_DB`,
   `POSTGRES_USER`, and `POSTGRES_PASSWORD` contain the correct values.
7. Apply the environment update and wait for the application to restart.
8. Test the health endpoint, authentication, and one complete create-and-read
   workout flow.
9. Keep the original instance until the restored application and its data have
   been verified.

## Point-in-time recovery

If automated backups are available, RDS can instead restore the database to a
specific time within the retention period. In the RDS console, choose
**Automated backups**, select the database, and choose **Restore to point in
time**. This also creates a new database instance, so use the same connection
and testing steps described above.

## Restore test

After the first production deployment, perform one test restore and connect a
non-production application environment to it. A backup is only trustworthy
after its restore procedure has been tested successfully.
