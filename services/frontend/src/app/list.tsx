"use client";
import { client } from "@/lib/api/client";

const List = () => {
  const { data, error } = client.useQuery("get", "/redirect_links/", {
    params: {
      query: {
        limit: 3,
        offset: 0,
      },
    },
  });

  if (error) {
    return <div>{JSON.stringify(error)}</div>;
  }

  return (
    <div>
      {data?.map((item) => {
        return (
          <div key={item.id}>
            {item.id} - {item.short_code} - {item.target_url}
          </div>
        );
      })}
    </div>
  );

};

export default List;
