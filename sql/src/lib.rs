use diesel::associations::HasTable;
use diesel::{ Connection, ExpressionMethods, PgConnection, RunQueryDsl };
use diesel::prelude::*;
use dotenvy::dotenv;
use std::env;

use self::models::*;

pub mod models;
pub mod schema;

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let db_url = env::var("DATABASE_URL")
        .expect("Failed to get url");

    PgConnection::establish(&db_url)
        .unwrap_or_else(|_| panic!("Error connecting to database"))
}

pub fn insert_news(title: &str, link: &str) -> News {
    use crate::schema::news;

    let connection = &mut establish_connection();

    let news = NewNews { title, link };

    diesel::insert_into(news::table)
        .values(&news)
        .on_conflict(schema::news::link)
        .do_update()
        .set((
            schema::news::title.eq(news.title),
            schema::news::link.eq(news.link)
        ))
        .returning(News::as_returning())
        .get_result(connection)
        .expect("Error saving news")
}

pub fn get_news(count: i64, offset: i64) -> Vec<News> {
    use self::schema::news::dsl::*;

    let connection = &mut establish_connection();
    
    news
        .select(News::as_select())
        .order_by(schema::news::id.desc())
        .limit(count)
        .offset(offset)
        .load(connection)
        .expect("Error loading news")
}

pub fn search(query: &str) -> Vec<News> {
    use self::schema::news::dsl::*;

    let connection = &mut establish_connection();

    let query = format!("%{query}%");
    
    news
        .select(News::as_select())
        .filter(schema::news::title.ilike(query))
        .order_by(schema::news::id.desc())
        .load(connection)
        .expect("Error loading news")
}

pub fn get_count() -> i64 {
    use self::schema::news::dsl::*;

    let connection = &mut establish_connection();

    news::table()
        .count()
        .get_result(connection)
        .expect("Error get size")
}