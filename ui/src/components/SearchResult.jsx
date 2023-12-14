import React from 'react'

export const SearchResult = ({pageTitle, url}) => {
  return (
    <div className='w-2/3 h-fit flex justify-start items-center m-4'>
    <a href={url} className='text-black font-bold'>{pageTitle}</a>
    </div>
  )
}
