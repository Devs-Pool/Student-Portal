#include<bits/stdc++.h>
using namespace std;
 #define ll long long 
// structure to hold queries
ll ans[200005];
struct Query
{
    ll l, r, x, idx;
};
 
// structure to hold array
struct ArrayElement
{
    ll val, idx;
};
 
// bool function to sort queries according to k
bool cmp1(Query q1, Query q2)
{
    return q1.x < q2.x;
}
 
// bool function to sort array according to its value
bool cmp2(ArrayElement x, ArrayElement y)
{
    return x.val < y.val;
}
 
// updating the bit array
void update(ll bit[], ll idx, ll val, ll n)
{
    for (; idx<=n; idx +=idx&-idx)
        bit[idx] += val;
}
 
// querying the bit array
ll query(ll bit[], ll idx, ll n)
{
    ll sum = 0;
    for (; idx > 0; idx -= idx&-idx)
        sum += bit[idx];
    return sum;
}
 
void answerQueries(ll n, Query queries[], ll q,
                              ArrayElement arr[])
{
    // initialising bit array
    ll bit[n+1];
    memset(bit, 0, sizeof(bit));
 
    // sorting the array
    sort(arr, arr+n, cmp2);
 
    // sorting queries
    sort(queries, queries+q, cmp1);
 
    // current index of array
    ll curr = 0;
 
    // array to hold answer of each Query
 
    // looping through each Query
    for (ll i=0; i<q; i++)
    {
        // traversing the array values till it
        // is less than equal to Query number
        while (arr[curr].val <= queries[i].x && curr<n)
        {
            // updating the bit array for the array index
            update(bit, arr[curr].idx+1, 1, n);
            curr++;
        }
 
        // Answer for each Query will be number of
        // values less than equal to x upto r minus
        // number of values less than equal to x
        // upto l-1
        ans[queries[i].idx] = query(bit, queries[i].r+1, n) -
                              query(bit, queries[i].l, n);
    }
 
  
}
 
// driver function
int main()
{
    // size of array
    ll n;
    cin>>n;
    // initialising array value and index
    ArrayElement arr[n];
    ll a[n];
    for(ll i=0;i<n;i++)
    {
        cin>>arr[i].val;
        arr[i].val--;
        a[i]=arr[i].val;
        arr[i].idx=i;
        // cout<<arr[i].val<<" "<<arr[i].idx<<endl;
    }
    ll q=n,k=0;
    Query queries[q];
    for(ll i=0;i<n-1;i++)
    {
        // cout<<arr[i].val<<" "<<arr[i].idx<<endl;
        if(arr[i].val<=(arr[i].idx))
        {
            continue;
        }
        else
        {
            queries[k].idx=k;
            queries[k].l=i+1;
            queries[k].r=min(n-1-i,arr[i].val);
            queries[k].x=i-1;
            // cout<<queries[k].idx<<" "<<queries[k].l<<" "<<queries[k].r<<" "<<queries[k].x<<endl;
            k++;
        }
    }
    // cout<<"bss "<<endl;
    answerQueries(n, queries, k, arr);
    long long cost=0;
    k=0;
    // for(ll i=0;i<n;i++)
    // {
    //  cout<<arr[i].val<<" "<<arr[i].idx<<endl;
    // }
    for(ll i=0;i<n-1;i++)
    {
        // cout<<arr[i].val<<" "<<arr[i].idx<<endl;
        if(a[i]<=i)
        {
            continue;
        }
        else
        {
            // cout<<"sda";
            // cout<<ans[k]<<endl;
            cost=cost+min(n-1-i,a[i])-ans[k];
            k++;
        }
    }
    cout<<cost<<endl;
    return 0;
}
